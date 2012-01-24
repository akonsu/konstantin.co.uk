# -*- mode:python; coding:utf-8; -*- Time-stamp: <urls.py - root>

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ko import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^contact/', views.ContactFormView.as_view(), name='contact'),
                       url(r'^projects/', views.ProjectsView.as_view(), name='projects'),
                       )

urlpatterns += staticfiles_urlpatterns()
