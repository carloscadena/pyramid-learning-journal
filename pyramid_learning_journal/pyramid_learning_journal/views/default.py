from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid_learning_journal.models import Journal


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """View for the home route."""
    session = request.dbsession
    all_journals = session.query(Journal).all()
    return {
        'page': 'Home',
        'journals': all_journals
    }


@view_config(route_name='detail', renderer="../templates/individual-entry.jinja2")
def detail_view(request):
    """View for the journal route."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entry = session.query(Journal).get(the_id)
    if not entry:
        raise HTTPNotFound

    return {
        'page': 'Journal Entry',
        'entry': entry
    }
