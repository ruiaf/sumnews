from django.template import RequestContext
from django.shortcuts import render

def homepage(request):
    news = [{'title': 'one piece of news title', 'content': 'a piece of news retrieved from the backend'},
            {'title': 'second piece of news title', 'content': 'another piece of news retrieved from the backend'}]
    context = RequestContext(request, {'news_list': news})
    return render(request, 'homepage.html', context)