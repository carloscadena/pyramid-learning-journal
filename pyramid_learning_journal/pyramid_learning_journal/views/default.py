import io
import os
from pyramid.response import Response

HERE = os.path.dirname(__file__)


def list_view(request):
    """List view"""
    with io.open(os.path.join(HERE, '../templates/index.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)


def detail_view(request):
    """Detail view"""
    with io.open(os.path.join(HERE, '../templates/individual-entry.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)


def create_view(request):
    """Create view"""
    with io.open(os.path.join(HERE, '../templates/new-entry.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)


def update_view(request):
    """update view"""
    with io.open(os.path.join(HERE, '../templates/edit.html')) as the_file:
        imported_text = the_file.read()

    return Response(imported_text)
