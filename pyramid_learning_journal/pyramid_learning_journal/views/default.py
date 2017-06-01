from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

JOURNALS = [
    {'id': 0, 'title': 'Week 3: Day 12', 'date': 'May 30, 2017', 'body': 'Today we started learning the pyramid framework. So far, its been easier to follow than building a server from scratch, but, its still been super confusing. David and I followed the instructions exactly as they were laid out and were able to accomlish our goals, but I dont feel like either of us have a great understanding of what parts are doing what. Personally, I have no idea what the changes I made to things did. I wish the purpose of each step was a little more apparent, but that might just be where my ability to understand is lacking.'},
    {'id': 1, 'title': 'Week 3: Day 11', 'date': 'May 31, 2017', 'body': """My journal isn't fully functional just yet so I'll write today's entry here and transfer it to that when it's operational. Today we learned about jinja, templating similar to handlebars. It's mostly straightforward and I feel OK about it. We also started the binary heap data structure but my partner and I weren't able to get started on that. I have a good idea how that's going to go."""},
    {'id': 2, 'title': 'Week 2: Day 10', 'date': 'May 26, 2017', 'body': """Today we learned about concurrency. I still need a lot of practice with everything to do with the server. We also had our first whiteboard challenge. It seemed pretty straight forward."""},
    {'id': 3, 'title': 'Week 2: Day 9', 'date': 'May 25, 2017', 'body': """Today we had an extra long, very helpful, code review. We added queue to the data structures we've learned, it wasn't terribly difficult to implement. So far, I'm enjoying data structures. Chris and I wrapped up part2 of the server projects. My understanding has come along way, but I'm still a ways from being able to build one solo."""},
    {'id': 4, 'title': 'Week 2: Day 8', 'date': 'May 24, 2017', 'body': """Today we learned about pytest fixtures, which I think I'm following correctly. The other subject we covered was super classes and the super function, I'm definitely less confident in this area. Working with the linked lists further solidified my understanding of them."""},
    {'id': 5, 'title': 'Week 2: Day 7', 'date': 'May 23, 2017', 'body': """Today we sorted out yesterday's sockets lab. Getting it to pass both versions of python involved a very unfamiliar looking set of instructions # -- coding: utf-8 -- I would not have been able to find my way to this bit of information on my own and it seems impressive to me that anyone found it. Sockets make a bit more sense to me today, though they're still very challenging."""},
    {'id': 6, 'title': 'Week 2: Day 6', 'date': 'May 22, 2017', 'body': """Day one week two was rough. Today we learned about sockets and most of the concepts have been difficult for me to grasp. We were also introduced to Linked Lists and I feel much more comfortable working out that logic."""},
    {'id': 7, 'title': 'Week 1: Day 5', 'date': 'May 19, 2017', 'body': """Today was really great practice. I wasn't terribly challenged by the katas I did, perhaps I should have tried more difficult ones, but I got so much practice with the python syntax and core methods. Writing all the tests wasn't fun but it was great to get into the flow of running the tests over and over. I wasn't looking forward to today when it was announced what we would be doing, but I really think I got a lot out of it and I'm glad we did it."""},
    {'id': 8, 'title': 'Week 1: Day 4', 'date': 'May 18, 2017', 'body': """Today I learned about creating a tox file and how to use it for testing. The lecture reinforced some understanding of lists, strings, tuples, and dictionaries. It also introduced new ideas, including using lambda functions to create small anonymous functions."""},
    {'id': 9, 'title': 'Week 1: Day 3', 'date': 'May 17, 2017', 'body': """Today I learned how to set up the setup.py file and how to use it. I also learned what 401 Python actually feels like. At least I think I did. I put in several extra hours and it still wasn't enough. Today's lab was rough, but we got super close to completing it."""},
    {'id': 10, 'title': 'Week 1: Day 2', 'date': 'May 16, 2017', 'body': """Today I learned a lot more about parameters. I wrote and ran the first few tests of my programing life. Using the local environment and running code in the command line became a little bit more clear to me."""},
    {'id': 11, 'title': 'Week 1: Day 1', 'date': 'May 15, 2017', 'body': """Today I learned that flow of Python is going to be a lot different from Javascript. I'm completely unfamiliar with the way we used the command line today and following along was difficult. I probably should have asked some questions but I wasn't sure where to even begin. Excited to figure it all out."""}

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
    journal = None
    try:
        journal = JOURNALS[the_id]
    except IndexError:
        raise HTTPNotFound

    return {
        'page': 'Journal Entry',
        'journal': journal
    }
