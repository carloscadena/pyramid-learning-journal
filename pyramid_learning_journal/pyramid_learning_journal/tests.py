# from pyramid import testing
import os
import io
# from pyramid.response import Response
# import pytest

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from pyramid_learning_journal.views.default import JOURNALS
import pytest


HERE = os.path.dirname(__file__)


@pytest.fixture
def httprequest():
    req = testing.DummyRequest()
    return req


def test_return_of_views_are_responses():
    """Test if the return of views are responses."""
    from pyramid_learning_journal.views.default import (
        list_view,
        detail_view,
        create_view,
        update_view
    )
    assert isinstance(list_view(httprequest), Response)
    assert isinstance(detail_view(httprequest), Response)
    assert isinstance(create_view(httprequest), Response)
    assert isinstance(update_view(httprequest), Response)


def test_html_content_in_response(httprequest):
    """Test the html content."""
    from pyramid_learning_journal.views.default import list_view
    file_content = io.open(os.path.join(HERE, 'templates/index.html')).read()
    response = list_view(httprequest)
    assert file_content == response.text


def check_if_ok_status_with_request(httprequest):
    """Check if 200 status on request."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(httprequest)
    assert response.status_code == 200

# =================== FUNCTIONAL TESTS =============


@pytest.fixture
def testapp():
    """Create a test application to use for functional tests."""
    from pyramid_learning_journal import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)


def test_home_route_returns_home_content(testapp):
    """Test the thome route returns home content."""
    response = testapp.get('/')
    html = response.html
    assert 'List of Journals' in str(html.find('h1').text)
    assert 'Journal Tracker | Home' in str(html.find('title').text)


def test_home_route_listing_has_all_journals(testapp):
    """Test the home route listing has all journals."""
    response = testapp.get('/')
    html = response.html
    assert len(JOURNALS) == len(html.find_all('li'))


def test_detail_route_with_bad_id(testapp):
    """Test the detail route with a bad ID."""
    response = testapp.get('/journal/400', status=404)
    assert "Alchemy scaffold" in response.text
