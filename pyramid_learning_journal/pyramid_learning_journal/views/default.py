from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )
from pyramid.security import remember, forget
from pyramid_learning_journal.models import Journal
from pyramid_learning_journal.security import check_credentials
import datetime


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """View for the home route."""
    session = request.dbsession
    all_journals = session.query(Journal).order_by(Journal.posted_date.desc()).all()
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


@view_config(
    route_name='create',
    renderer='../templates/new-entry.jinja2',
    permission="secret"
)
def create_view(request):
    """View for adding new entries to journal"""
    if request.method == "POST":
        if not request.POST['title'] or not request.POST['body']:
            return {
                'title': request.POST['title'],
                'body': request.POST['body']
            }
        new_entry = Journal(
            title=request.POST['title'],
            body=request.POST['body'],
            posted_date=datetime.datetime.now()
        )
        request.dbsession.add(new_entry)
        return HTTPFound(
            location=request.route_url('home')
        )

    return {}


@view_config(
    route_name="update",
    renderer="../templates/new-entry.jinja2",
    permission='secret'
    )
def update_view(request):
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entry = session.query(Journal).get(the_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            'page': "Edit this journal entry",
            'title': entry.title,
            'body': entry.body
        }

    if request.method == 'POST':
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=entry.id))


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    """View for logging in a user."""
    if request.method == 'GET':
        return {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(
                location=request.route_url('home'),
                headers=headers
            )
        return{'error': 'Bad username or password'}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
