import os
import io
import pytest
from pyramid import testing
import transaction
from pyramid_learning_journal.models import (
    Journal,
    get_tm_session
)
from pyramid_learning_journal.models.meta import Base
from faker import Faker
import random
import datetime

FAKE_FACTORY = Faker()
CATEGORIES = ["rent", "utilities", "groceries", "food", "netflix", "booze"]
JOURNAL_LIST = [Journal(
    title=random.choice(CATEGORIES),
    posted_date=datetime.datetime.now(),
    body=FAKE_FACTORY.text(50),
) for i in range(10)]


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.
    Every test that includes this fixture will add new random expenses.
    """
    dummy_request.dbsession.add_all(JOURNAL_LIST)


@pytest.fixture(scope="session")
def configuration(request):
    """
    Set up a Configurator instance.
    This Configurator instance sets up a pointer to the location of the database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres:///journal_test_db'
    })
    config.include("pyramid_learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.
    This uses the dbsession_factory on the configurator instance
    to create a new database session. It binds that session to the available
    engine and returns a new session for every call of the dumm_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.binds
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


def test_model_gets_added(db_session):
    assert len(db_session.query(Journal).all()) == 0
    model = Journal(
        title="title filler",
        posted_date=datetime.datetime.now(),
        body="fake body content"
    )
    db_session.add(model)
    assert len(db_session.query(Journal).all()) == 1


@pytest.fixture
def testapp():
    """Create a test application to use for functional tests."""
    from webtest import TestApp
    from pyramid_learning_journal import main

    app = main({}, **{"sqlalchemy.url": "postgres:///journal_test_db"})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(JOURNAL_LIST)

    return dbsession


def test_home_route_returns_home_content(dummy_request):
    """Home view returns a dictionary of values."""
    from pyramid_learning_journal.views.default import home_view
    response = home_view(dummy_request)
    assert isinstance(response, dict)


def test_home_view_returns_empty_when_database_empty(dummy_request):
    """Home view returns nothing when there is no data."""
    from pyramid_learning_journal.views.default import home_view
    response = home_view(dummy_request)
    assert len(response['journals']) == 0


def test_home_view_returns_count_matching_database(testapp):
    """Home view response mathes database count."""
    from pyramid_learning_journal.view.default import home_view
    response = home_view(dummy_request)
    query = dummy_request.dbsession.query(Journal)
    assert len(response['journals']) == query.count()



# def test_detail_route_with_bad_id(testapp):
#     """Test the detail route with a bad ID."""
#     response = testapp.get('/journal/400', status=404)
#     assert "Alchemy scaffold" in response.text
