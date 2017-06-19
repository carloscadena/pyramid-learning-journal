"""Testing for Learning Journal"""
import pytest
from pyramid import testing
import transaction
import os
from pyramid_learning_journal.models import (
    Journal,
    get_tm_session
)
from pyramid_learning_journal.models.meta import Base
import faker
import datetime


@pytest.fixture(scope="session")
def configuration(request):
    """
    Set up a Configurator instance.
    This Configurator instance sets up a pointer to the location of the database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    settings = {
        'sqlalchemy.url': os.environ.get('DATABASE_URL_TEST')
    }
    config = testing.setUp(settings=settings)
    config.include("pyramid_learning_journal.models")
    config.include('pyramid_learning_journal.routes')

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
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    req = testing.DummyRequest()
    req.dbsession = db_session
    return req


@pytest.fixture
def post_request(dummy_request):
    dummy_request.method = "POST"
    return dummy_request


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.
    Every test that includes this fixture will add new random expenses.
    """
    dummy_request.dbsession.add_all(JOURNAL_LIST)


@pytest.fixture
def set_auth_credentials():
    """Make a username/password combo for testing."""
    import os
    from passlib.apps import custom_app_context as pwd_context

    os.environ["SESSION_SECRET"] = "hellothere"
    os.environ["AUTH_USERNAME"] = "test"
    os.environ["AUTH_PASSWORD"] = pwd_context.hash("testpw")


@pytest.fixture(scope="session")
def testapp(request):
    """Create a test application to use for functional tests."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """
        settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL_TEST')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.include('.security')
        config.scan()
        return config.make_wsgi_app()

    app = main({})
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


# This is a Faker object for giving us fake data
FAKE = faker.Faker()

JOURNAL_LIST = [Journal(
    title=FAKE.name(),
    posted_date=datetime.datetime.now(),
    body=FAKE.text(50),
) for i in range(20)]


# =========== Unit Tests ===============

def test_new_journal_entries_are_added(db_session):
    """Test that new Journal entries are added to the DB"""
    db_session.add_all(JOURNAL_LIST)
    query = db_session.query(Journal).all()
    assert len(query) == len(JOURNAL_LIST)


def test_model_gets_added(db_session):
    assert len(db_session.query(Journal).all()) == 0
    model = Journal(
        title=u"title filler",
        posted_date=datetime.datetime.now(),
        body=u"fake body content"
    )
    db_session.add(model)
    assert len(db_session.query(Journal).all()) == 1


def test_home_view_returns_empty_when_empty(dummy_request):
    """Test the home view returns no objects in ____ iterable"""
    from .views.default import home_view
    result = home_view(dummy_request)
    assert len(result['journals']) == 0


def test_home_view_returns_objects_when_they_exist(dummy_request, add_models):
    """Test that the home view does return object when the DB is populated."""
    from .views.default import home_view
    result = home_view(dummy_request)
    assert len(result['journals']) == 20


def test_home_route_returns_home_content(dummy_request):
    """Home view returns a dictionary of values."""
    from pyramid_learning_journal.views.default import home_view
    response = home_view(dummy_request)
    assert isinstance(response, dict)


def test_home_view_returns_count_matching_database(dummy_request):
    """Home view response mathes database count."""
    from pyramid_learning_journal.views.default import home_view
    response = home_view(dummy_request)
    query = dummy_request.dbsession.query(Journal)
    assert len(response['journals']) == query.count()


def test_detail_route_with_bad_id(testapp):
    """Test the detail route with a bad ID."""
    response = testapp.get('/journal/87263', status=404)
    assert response.status_code == 404


def test_detail_view_contains_individual_journal_details(db_session, dummy_request, add_models):
    """Test that the detail view actually returns individual journal entry"""
    from .views.default import detail_view
    dummy_request.matchdict["id"] = 12
    journal = db_session.query(Journal).get(12)
    result = detail_view(dummy_request)
    assert result["entry"] == journal


def test_create_view_post_empty_data_returns_empty_dict(post_request):
    from pyramid_learning_journal.views.default import create_view
    post_request.POST = {
        'title': '',
        'body': ''
    }
    response = create_view(post_request)
    assert response == {'title': '', 'body': ''}


def test_create_view_post_incomplete_data_returns_data(post_request):
    from pyramid_learning_journal.views.default import create_view
    data = {
        'title': u'not in the db',
        'body': ''
    }
    post_request.POST = data
    response = create_view(post_request)
    assert 'title' in response
    assert 'body' in response
    assert response['title'] == 'not in the db'


def test_create_view_post_with_data_redirects(post_request):
    from pyramid_learning_journal.views.default import create_view
    from pyramid.httpexceptions import HTTPFound
    data = {
        'title': u'a title here',
        'body': u'some text in the body'
    }
    post_request.POST = data
    response = create_view(post_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_create_view_post_request_adds_new_db_item(db_session, dummy_request):
    """Posting to the create view adds an item."""
    from .views.default import create_view

    dummy_request.method = "POST"
    dummy_request.POST["title"] = u"this new entry"
    dummy_request.POST["body"] = u"some text in the body"
    create_view(dummy_request)
    new_entry = db_session.query(Journal).first()
    assert new_entry.title == "this new entry"
    assert new_entry.body == "some text in the body"

SITE_ROOT = 'http://localhost'

def test_new_entry_redirects_to_home(testapp):
    """When redirect happens after new entry, result is home page"""
    data = {
        'title': u"fake titles are the best",
        'body': u'fake body text is fake body text'
    }
    response = testapp.post('/journal/new-entry', data)
    assert response.location == SITE_ROOT + '/'


def test_update_view_returns_entry_info(db_session, dummy_request, add_models):
    """Get requet to the update view contains journal entry info."""
    from .views.default import update_view
    # import pdb; pdb.set_trace()
    dummy_request.matchdict["id"] = 2
    result = update_view(dummy_request)
    journal_entry = db_session.query(Journal).get(2)
    assert result['title'] == journal_entry.title


def test_login_view_get_request(dummy_request):
    """Test that you can see the login view."""
    from .views.default import login
    result = login(dummy_request)
    assert result == {}


def test_login_view_good_credentials(dummy_request, set_auth_credentials):
    """Test that when given good credentials login can be successful."""
    from .views.default import login
    from pyramid.httpexceptions import HTTPFound
    dummy_request.method = "POST"
    dummy_request.POST["username"] = "test"
    dummy_request.POST["password"] = "testpw"
    result = login(dummy_request)
    assert isinstance(result, HTTPFound)
