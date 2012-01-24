# -*- mode:python; coding:utf-8; -*- Time-stamp: <bootstrap.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

import os

path = os.path.abspath(os.path.dirname(__file__))

while not os.path.exists(os.path.join(path, 'settings.py')):
    parent = os.path.abspath(os.path.join(path, '..'))

    if path == parent:
        raise Exception('cannot find settings.py')

    path = parent

os.sys.path.append(path)

import settings
from django.core import management

management.setup_environ(settings)
