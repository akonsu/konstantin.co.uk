import os
import sys

from django.core.handlers.wsgi import WSGIHandler

sys.path = ['/home2/akonsu/webapps/custom/sites/konstantin_co_uk/'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = WSGIHandler()
