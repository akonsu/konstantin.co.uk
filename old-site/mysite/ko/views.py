# -*- mode:python; coding:utf-8; -*- Time-stamp: <views.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.generic.list_detail import object_list
from ko.loader import *
from ko.models import *
from tagging.views import tagged_object_list

def enum_thumbnails(request):
    def get_int_param(request, name):
        try:
            return int(request.REQUEST.get(name, 0))
        except ValueError:
            raise Http404

    def get_plate_data(plate):
        d = {'link': {'href': plate.get_absolute_url()}}
        t = plate.get_thumbnail()

        if t:
            d['thumbnail'] = {'alt': plate.name, 'height': t.height, 'src': t.content.url, 'width': t.width}

        return d

    count = get_int_param(request, 'count')
    offset = get_int_param(request, 'offset')
    data = [get_plate_data(p) for p in Plate.objects.filter(name__startswith='unfocused')[offset: offset + count]]

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def index(request):
    plates = Plate.objects.filter(parents=None)
    return object_list(request, plates, paginate_by=5, template_name='index.html')

def view_plate(request, name):
    extra_context = {'plate': get_object_or_404(Plate, name=name)}
    return render_to_response('plate.html', extra_context, context_instance=RequestContext(request))

def view_plate_list(request, tag):
    return tagged_object_list(request, Plate, tag, paginate_by=30, template_loader=Loader(tag), template_name='plate_list.html')

def view_selected_plate(request, tag, name):
    extra_context = {'selected': get_object_or_404(Plate, name=name)}
    return tagged_object_list(request, Plate, tag, template_loader=Loader(tag), template_name='plate_list.html', extra_context=extra_context)
