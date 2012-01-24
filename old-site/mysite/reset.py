#!/usr/bin/env python2.6
# -*- mode:python; coding:utf-8; -*- Time-stamp: <reset.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

import scripts.bootstrap

import email
import Image
import ImageColor
import os
import re
import scripts.utils as utils
import settings
import string

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import management
from ko.fixtures import *
from ko.models import Part, Plate, PlatePart
from scripts.submit import process_submission
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError

def __main__():
    #<!-- plate <tuple> -->
    PLATE_DECL_RE = re.compile(r'^\s*<!--\s*plate\s+(.*)\s*-->\s*$')

    print 'flushing...'
    management.call_command('flush', interactive=False)

    dependencies = []

    for root, dirs, files in os.walk('ko/fixtures'):
        for x in files:
            if x.endswith('.template'):
                with open(os.path.join(root, x)) as fp:
                    current = []
                    reset = False
                    template = ''

                    print '%s:' % x

                    for line in fp:
                        m = PLATE_DECL_RE.search(line)

                        if m:
                            if reset:
                                for t in current:
                                    plate = create_plate(t, template, dependencies)
                                    print plate

                                current = []
                                reset = False
                                template = ''

                            current.append(eval(*m.groups()))

                        else:
                            reset = True
                            template += line

                    for t in current:
                        plate = create_plate(t, template, dependencies)
                        print plate

                print

    for plate, plates in dependencies:
        if len(plates) > 0:
            print plate, plates

        for name in plates:
            plate.plates.add(Plate.objects.get(name=name))

    user = User(username='root', password=settings.ADMIN_PASSWORD)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print 'user=%s' % user

    site = Site.objects.get_current()
    site.domain = 'konstantin.co.uk'
    site.name = site.domain
    site.save()
    print 'site=%s' % site

    for root, dirs, files in os.walk('ko/fixtures/submissions'):
        for x in files:
            if x.endswith('.email'):
                with open(os.path.join(root, x), 'rb') as fp:
                    message = email.message_from_file(fp)

                    print 'submission %s' % message['subject']
                    process_submission(message)

def add_part(plate, item):
    if isinstance(item, tuple):
        base_name, attr_name, w, h = item
        file_name = scale_image(base_name, w, h)
        part_name = file_name.translate(string.maketrans('.-', '__'))

    else:
        file_name = item
        part_name = file_name.translate(string.maketrans('.-', '__'))
        attr_name = '__%s' % part_name

    w, h = get_image_size(file_name) or (0, 0)
    part, _ = Part.objects.get_or_create(name=part_name, defaults={'content': file_name, 'height': h, 'width': w})

    return PlatePart.objects.create(name=attr_name, part=part, plate=plate)

def create_plate(t, templates, dependencies):
    name, date, tags, parts, plates = t
    dtime = utils.TruncatedDateTime(date)
    plate = Plate.objects.create(datetime=dtime.value, name=name, precision=dtime.precision, tags=tags)
    root = None

    try:
        root = ElementTree.XML(templates)

    except ExpatError:
        pass

    if root and root.tag == 'templates':
        for x in root:
            plate.templates.create(name=x.tag, text=x.text)

    else:
        plate.templates.create(name='default', text=templates)

    dependencies.append((plate, plates))

    for x in parts:
        add_part(plate, x)

    return plate

def get_image_size(name):
    try:
        image = Image.open(os.path.join(settings.MEDIA_ROOT, name))
        return image.size

    except IOError:
        pass

    return None

def scale_image(name, w, h):
    result_name = '_%dx%d_%s' % (w, h, name)
    path = os.path.join(settings.MEDIA_ROOT, result_name)

    if not os.path.isfile(path):
        image = Image.open(os.path.join(settings.MEDIA_ROOT, name))

        image.thumbnail((w, h), Image.ANTIALIAS)
        image.save(path, optimize=True, quality=75)

    return result_name

if __name__ == '__main__':
    __main__()
