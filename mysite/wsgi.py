# -*- mode:python; coding:utf-8; -*- Time-stamp: <wsgi.py - root>

import os
import sys

sys.path = ['/home/akonsu/webapps/custom/sites/konstantin_co_uk/'] + sys.path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
