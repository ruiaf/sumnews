from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.views import *
from sumnews.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', clusters),
    url(r'^latest/$', latest),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^signup/$', signup),
    url(r'^debug/$', debug),
    url(r'^edition/(?P<edition>.*)/$', set_edition),
    url(r'^search/(?P<query>.*)/$', search),
    url(r'^article/(?P<edition>.*)/(?P<guid>.*)/$', article),
)