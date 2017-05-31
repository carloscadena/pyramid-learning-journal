from pyramid import testing
import os
import io
from pyramid.response import Response
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
