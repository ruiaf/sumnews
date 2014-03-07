from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'coreux.sumnews.views.homepage', name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
)