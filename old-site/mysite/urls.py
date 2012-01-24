# -*-python-*- Time-stamp: <urls.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from ko.feeds import BlogFeed

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', 'ko.views.index'),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'index.html'}),
                       (r'^p/([^/]+)/$', 'ko.views.view_plate'),
                       (r'^t/(?P<tag>[^/]+)/$', 'ko.views.view_plate_list'),
                       (r'^t/([^/]+)/([^/]+)/$', 'ko.views.view_selected_plate'),
                       url(r'^f/blog/$', BlogFeed(), name='blog-feed'),
                       (r'^api/t/$', 'ko.views.enum_thumbnails'),
                       (r'^admin/', include(admin.site.urls)),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'ko/media'}),
                            )
