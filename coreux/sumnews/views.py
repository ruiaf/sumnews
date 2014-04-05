from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from beinterface.beinterface import BackendInterface
from coreux import settings
import random


def set_edition(request, edition):
    validated_edition = None
    for (e, e_name) in settings.editions:
        if e == edition:
            validated_edition = edition

    if validated_edition:
        request.session['edition'] = edition

    return redirect('/')

def clusters(request):
    response = BackendInterface.retrieve({"type": "latest_clusters", "edition": request.session['edition']})
    context = RequestContext(request, {'cluster_list': response["content"]})
    return render(request, 'cluster_list.html', context)

def latest(request):
    response = BackendInterface.retrieve({"type": "latest_news", "edition": request.session['edition']})
    context = RequestContext(request, {'news_list': response["content"]})
    return render(request, 'news_list.html', context)

def search(request, query):
    if query is None or len(query.strip()) == 0:
        return HttpResponseRedirect("/")
    response = BackendInterface.retrieve({"type": "search_clusters", "edition": request.session['edition'], "query": query})
    context = RequestContext(request, {'cluster_list': response["content"]})
    return render(request, 'cluster_list.html', context)

def article(request, edition, guid):
    if guid is None or len(guid.strip()) == 0:
        return HttpResponseRedirect("/")
    response = BackendInterface.retrieve({"type": "search_guid", "edition": edition, "guid": guid})
    context = RequestContext(request, response["content"])
    return render(request, 'article.html', context)

def debug(request):
    stats = BackendInterface.retrieve({"type": "stats", "edition": request.session['edition']})
    latest_clusters = BackendInterface.retrieve({"type": "latest_clusters", "edition": request.session['edition']})

    graph = { "nodes": [], "edges": []}
    i = 0
    for cluster in latest_clusters["content"]:
        node = {
            "id": str(i),
            "label": "", #doc["title"],
            "x": random.random()*10,
            "y": random.random()*10,
            "size": 0.001
        }
        graph["nodes"].append(node)

        for doc in cluster:
            node = {
                "id": doc["guid"],
                "label": "", #doc["title"],
                "x": random.random()*10,
                "y": random.random()*10,
                "size": 0.001
            }
            graph["nodes"].append(node)

            edge = {
                "id": str(i) + doc["guid"],
                "source": doc["guid"],
                "target": str(i),
                "size": random.random()
            }
            graph["edges"].append(edge)
        i += 1

    context = RequestContext(request, {'stats': stats["content"], "graph": graph})
    return render(request, 'debug.html', context)