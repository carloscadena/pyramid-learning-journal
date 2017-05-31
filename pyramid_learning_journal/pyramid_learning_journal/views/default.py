
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

JOURNALS = [
    {'id': 0, 'title': 'Journal Entry 1', 'date': 'May 30, 2017', 'body': 'Today we started learning the pyramid framework. So far, its been easier to follow than building a server from scratch, but, its still been super confusing. David and I followed the instructions exactly as they were laid out and were able to accomlish our goals, but I dont feel like either of us have a great understanding of what parts are doing what. Personally, I have no idea what the changes I made to things did. I wish the purpose of each step was a little more apparent, but that might just be where my ability to understand is lacking.'},
    {'id': 1, 'title': 'Journal Entry 2', 'date': 'May 01, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 2, 'title': 'Journal Entry 3', 'date': 'May 02, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 3, 'title': 'Journal Entry 4', 'date': 'May 05, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 4, 'title': 'Journal Entry 5', 'date': 'May 09, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'id': 5, 'title': 'Journal Entry 6', 'date': 'May 12, 2017', 'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'}
]


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """View for the home route."""
    return {
        'page': 'Home',
        'journals': JOURNALS
    }

@view_config(route_name='detail', renderer="../templates/individual-entry.jinja2")
def detail_view(request):
    """View for the journal route."""
    the_id = int(request.matchdict['id'])
    try:
        journal = JOURNALS[the_id]
    except IndexError:
        raise HTTPNotFound

    return {
        'page': 'Journal Entry',
        'journal': journal
    }


# import io
# import os
# from pyramid.response import Response
#
# HERE = os.path.dirname(__file__)
#
#
# def list_view(request):
#     """List view"""
#     with io.open(os.path.join(HERE, '../templates/index.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
#
#
# def detail_view(request):
#     """Detail view"""
#     with io.open(os.path.join(HERE, '../templates/individual-entry.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
#
#
# def create_view(request):
#     """Create view"""
#     with io.open(os.path.join(HERE, '../templates/new-entry.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
#
#
# def update_view(request):
#     """update view"""
#     with io.open(os.path.join(HERE, '../templates/edit.html')) as the_file:
#         imported_text = the_file.read()
#
#     return Response(imported_text)
