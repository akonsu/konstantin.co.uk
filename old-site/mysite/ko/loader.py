# -*-python-*- Time-stamp: <loader.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

from django.template import loader
from os import path

class Loader(object):
    def __init__(self, tag):
        self.tag = tag

    def get_template(self, template_name):
        head, tail = path.split(template_name)
        names = [path.join(head, '%s_%s' % (self.tag, tail)), template_name]
        return loader.select_template(names)
