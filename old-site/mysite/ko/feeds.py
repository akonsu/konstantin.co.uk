# -*-python-*- Time-stamp: <feeds.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from ko.models import Plate

class BlogFeed(Feed):
    link = "/f/blog/"
    title = '%s-web-log' % Site.objects.get_current()

    def items(self):
        return Plate.objects.filter(parents=None)[:5]
