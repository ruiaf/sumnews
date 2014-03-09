from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from beinterface.beinterface import BackendInterface

def homepage(request):
    response = BackendInterface.retrieve({"type": "latest_news"})
    context = RequestContext(request, {'news_list': response["content"]})
    return render(request, 'news_list.html', context)

def search(request, query):
    if query is None or len(query.strip()) == 0:
        return HttpResponseRedirect("/")
    response = BackendInterface.retrieve({"type": "search", "query": query})
    context = RequestContext(request, {'news_list': response["content"]})
    return render(request, 'news_list.html', context)