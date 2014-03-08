from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sumnews.views.homepage', name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^signup/$', signup),
)