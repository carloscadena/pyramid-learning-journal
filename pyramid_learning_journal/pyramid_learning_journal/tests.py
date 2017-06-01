import os
import io
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from pyramid_learning_journal.views.default import JOURNALS
import pytest


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
    assert 'Python 401 Learning Journal' in str(html.find('title').text)


def test_home_route_listing_has_all_journals(testapp):
    """Test the home route listing has all journals."""
    response = testapp.get('/')
    html = response.html
    assert len(JOURNALS) == len(html.find_all('li'))


def test_detail_route_with_bad_id(testapp):
    """Test the detail route with a bad ID."""
    response = testapp.get('/journal/400', status=404)
    assert "Alchemy scaffold" in response.text
