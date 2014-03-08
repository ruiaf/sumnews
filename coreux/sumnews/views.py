from django.template import RequestContext
from django.shortcuts import render
from datetime import datetime, timedelta

def homepage(request):
    news = [{'title': 'one piece of news title', 'date': datetime.now() - timedelta(minutes = 10), 'content': 'a piece of news retrieved from the backend'},
            {'title': 'second piece of news title', 'date': datetime.now() - timedelta(hours = 50), 'content': 'another piece of news retrieved from the backend'}]
    context = RequestContext(request, {'news_list': news})
    return render(request, 'homepage.html', context)