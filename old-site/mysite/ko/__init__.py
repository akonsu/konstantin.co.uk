# -*-python-*- Time-stamp: <__init__.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

from django import template
from django.core.paginator import Paginator

class PaginatorMixin:
    def digg_page_range(self, page):
        BODY_PAGES = 9
        MARGIN_PAGES = 3
        TAIL_PAGES = 2

        position = 1

        p, q = TAIL_PAGES, max(1, min(page.number - BODY_PAGES / 2, self.num_pages - BODY_PAGES + 1))

        if q - p > MARGIN_PAGES:
            for x in xrange(position, p + 1):
                yield x

            yield None

            position = q

        p, q = q + BODY_PAGES - 1, self.num_pages - TAIL_PAGES + 1

        if q - p > MARGIN_PAGES:
            for x in xrange(position, p + 1):
                yield x

            yield None

            position = q

        for x in xrange(position, self.num_pages + 1):
            yield x

if PaginatorMixin not in Paginator.__bases__:
    Paginator.__bases__ = (PaginatorMixin,) + Paginator.__bases__

template.add_to_builtins('ko.templatetags.customtags')
