from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from beinterface.beinterface import BackendInterface


def clusters(request):
    response = BackendInterface.retrieve({"type": "latest_clusters"})
    context = RequestContext(request, {'cluster_list': response["content"]})
    return render(request, 'cluster_list.html', context)

def latest(request):
    response = BackendInterface.retrieve({"type": "latest_news"})
    context = RequestContext(request, {'news_list': response["content"]})
    return render(request, 'news_list.html', context)

def search(request, query):
    if query is None or len(query.strip()) == 0:
        return HttpResponseRedirect("/")
    response = BackendInterface.retrieve({"type": "search_clusters", "query": query})
    context = RequestContext(request, {'cluster_list': response["content"]})
    return render(request, 'cluster_list.html', context)

def article(request, guid):
    if guid is None or len(guid.strip()) == 0:
        return HttpResponseRedirect("/")
    response = BackendInterface.retrieve({"type": "search_guid", "guid": guid})
    context = RequestContext(request, response["content"])
    return render(request, 'article.html', context)