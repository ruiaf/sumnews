from django.conf.urls import patterns, url

from coreux.news import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)