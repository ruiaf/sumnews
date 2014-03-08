from django.template import RequestContext
from django.shortcuts import render
from beinterface.beinterface import BackendInterface

def homepage(request):
    response = BackendInterface.retrieve({"type": "latest_news"})
    context = RequestContext(request, {'news_list': response["content"]})
    return render(request, 'homepage.html', context)