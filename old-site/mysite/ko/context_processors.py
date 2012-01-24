# -*-python-*- Time-stamp: <context_processors.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

def media_url(request):
    from django.conf import settings
    return {'media_url': settings.MEDIA_URL}
