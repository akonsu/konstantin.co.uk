#!/usr/bin/env python2.6
# -*- mode:python; coding:utf-8; -*- Time-stamp: <submit.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

import bootstrap

import collections
import email
import gpgmail
import Image
import logging
import os
import re
import settings
import sys
import traceback
import utils
import uuid

from contextlib import *
from cStringIO import StringIO
from django.db import transaction
from email.message import Message
from ko.models import *
from pyparsing import *

local_files = []

def __main__():
    handler = utils.AdminMailingHandler()
    logger = logging.getLogger()

    handler.setFormatter(logging.Formatter('%(module)s:%(levelname)s:%(message)s'))
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    try:
        with open(save_stdin(), 'rb') as fp:
            message = email.message_from_file(fp)

        subject = message['subject']
        handler.subject = 'RE: %s' % subject

        logger.info('parsed email message %s' % subject)
        process_submission(message)

    except:
        try:
            strings = ['\n'] + traceback.format_exception(*sys.exc_info())
            logger.critical(''.join(strings).replace('\n', '\n\t').strip())
        except:
            pass

def create_child_plate(message, file_name, image_data, image_attrs, default_attrs):
    IMAGE_DISPLAY_SIZE = (300, 300)
    IMAGE_FULL_SIZE = (650, 650)
    IMAGE_THUMBNAIL_SIZE = (150, 150)

    DIV = lambda text: r'<div>%s</div>' % text
    TEMPLATE = '''
      <div>
        <div style="float:left;">
          {%% with self.content_parts.0 as p %%}
            <img alt="{{self.name}}" src="{{p.content.url}}" width="{{p.width}}px" height="{{p.height}}px" />
          {%% endwith %%}
        </div>
        <div class="nobr" style="float:left;padding-left:50px;">
          <div class="plate-title">{{self.name}}</div>
          <div>{{self.datetime_display}}</div>
          %s%s
        </div>
        <div style="clear:both;" />
      </div>
      '''

    dtime = utils.TruncatedDateTime(image_attrs['date'] if 'date' in image_attrs \
                                    else default_attrs['date'] if 'date' in default_attrs \
                                    else utils.get_email_datetime(message))
    medium = DIV(image_attrs['medium']) if 'medium' in image_attrs \
             else DIV(default_attrs['medium']) if 'medium' in default_attrs \
             else ''
    size = DIV(image_attrs['size']) if 'size' in image_attrs \
           else DIV(default_attrs['size']) if 'size' in default_attrs \
           else ''

    name = slugify(os.path.splitext(file_name)[0])
    tags = image_attrs.get('tags')

    plate = Plate.objects.create(datetime=dtime.value, name=name, precision=dtime.precision, tags=tags)
    logging.info('created plate %s' % plate)

    display_part = create_part(image_data, 'd', file_name, IMAGE_DISPLAY_SIZE)
    full_part = create_part(image_data, '', file_name, IMAGE_FULL_SIZE)
    thumbnail_part = create_part(image_data, 't', file_name, IMAGE_THUMBNAIL_SIZE)

    default_template = plate.templates.create(name='default', text=TEMPLATE % (medium, size))
    logging.info('created template %s' % default_template)

    display_platepart = PlatePart.objects.create(name='display', part=display_part, plate=plate)
    logging.info('created plate-part dependency %s' % display_platepart)

    full_platepart = PlatePart.objects.create(name='__%s' % full_part.name, part=full_part, plate=plate)
    logging.info('created plate-part dependency %s' % full_platepart)

    thumbnail_platepart = PlatePart.objects.create(name='thumbnail', part=thumbnail_part, plate=plate)
    logging.info('created plate-part dependency %s' % thumbnail_platepart)

    return plate

def create_main_plate(message, text, attachments, attributes):
    TEMPLATE = '''
      %s
      <br /><br />
      <div>
        {%% for p in self.plates.all %%}
          {%% with p.get_%s as x %%}
            <a href="{%% url ko.views.view_plate p.name %%}">
              <img alt="{{p.name}}" src="{{x.content.url}}" width="{{x.width}}px" height="{{x.height}}px" /></a>
          {%% endwith %%}
        {%% endfor %%}
      </div>
      '''

    default_attrs = attributes['']

    dtime = utils.TruncatedDateTime(default_attrs['date'] if 'date' in default_attrs else utils.get_email_datetime(message))
    name = message['subject']
    tags = default_attrs.get('tags')

    plate = Plate.objects.create(datetime=dtime.value, name=name, precision=dtime.precision, tags=tags)
    logging.info('created plate %s' % plate)

    default_template = plate.templates.create(name='default', text=TEMPLATE % (text, 'display'))
    logging.info('created template %s' % default_template)

    summary_template = plate.templates.create(name='summary', text=TEMPLATE % (text, 'thumbnail'))
    logging.info('created template %s' % summary_template)

    for k, v in attachments.iteritems():
        file_name = os.path.basename(k)
        image_data = v.get_payload(decode=True)
        child_plate = create_child_plate(message, file_name, image_data, attributes[k], default_attrs)

        plate.plates.add(child_plate)
        logging.info('created dependency %s->%s' % (plate, child_plate))

    return plate

def create_part(image_data, name_prefix, file_name, size):
    part_name = name_prefix + slugify(file_name)

    relative_dir = '%dx%d' % size
    relative_path = os.path.join(relative_dir, file_name)

    full_dir = os.path.abspath(os.path.join(settings.MEDIA_ROOT, relative_dir))
    full_path = os.path.join(full_dir, file_name)

    global local_files
    local_files.append(full_path)

    try:
        os.makedirs(full_dir)
        logging.info('created path %s' % full_dir)
    except os.error:
        pass

    with closing(StringIO(image_data)) as s:
        image = Image.open(s)

        w, h = image.size
        W, H = size

        if w > W or h > H:
            image.thumbnail(size, Image.ANTIALIAS)

            w, h = image.size
            part = Part.objects.create(name=part_name, content=relative_path, height=h, width=w)
            logging.info('created part %s' % part)

            image.save(full_path, 'JPEG')
            logging.info('saved image %s' % full_path)
        else:
            part = Part.objects.create(name=part_name, content=relative_path, height=h, width=w)
            logging.info('created part %s' % part)

            with open(full_path, 'wb') as fp:
                fp.write(image_data)

            logging.info('saved image %s' % full_path)

    return part

def parse(text):
    filename = Optional(Word(alphanums + '-._') + Suppress(':')).setParseAction(lambda t: t or '')
    slug = Word(alphanums + '-_')
    string = quotedString.setParseAction(removeQuotes)

    attribute = (filename + (string | slug)).setParseAction(lambda t: tuple(t))
    attributes = (Combine(Suppress('@') + slug) + Suppress('=') + delimitedList(attribute)).setResultsName('attributes', listAllMatches=True)

    grammar = SkipTo(ZeroOrMore(attributes) + StringEnd(), include=True)

    return grammar.parseString(text)[0]

@transaction.commit_on_success
def process_submission(message):
    with utils.call_on_error(unlink_files):
        for verified, contents in gpgmail.signed_parts(message):
            if verified and verified.fingerprint.lower() == 'a3458ea35d42e446fae20427194c473e68cbc220':
                logging.info('verified key %s' % verified.fingerprint)

                attachments = {}
                text = ''

                if isinstance(contents, Message):
                    for part in gpgmail.filter_parts(contents, lambda m: not m.is_multipart()):
                        t = part.get_content_type()

                        if t == 'text/plain':
                            text += part.get_payload(decode=True)

                        elif t == 'image/jpeg':
                            name = part.get_filename() or part.get_param('name')

                            if name:
                                attachments[name] = part
                else:
                    text = contents

                logging.info('found attachments %s' % attachments.keys())

                tokens = parse(text)
                attributes = read_attributes(tokens, attachments)

                create_main_plate(message, tokens[0], attachments, attributes)

def read_attributes(tokens, attachments):
    d = collections.defaultdict(dict)

    logging.info('parsed attributes %s' % [x[0] for x in tokens.attributes])

    for t in tokens.attributes:
        s = t[0]

        for k, v in t[1:]:
            if k and k not in attachments:
                raise Exception, 'cannot find attachment %s' % k
            d[k][s] = v

    return d

def save_stdin():
    settings_dir = os.path.dirname(settings.__file__)
    full_dir = os.path.abspath(os.path.join(settings_dir, 'ko', 'fixtures', 'submissions'))
    full_path = os.path.join(full_dir, '%s.email' % uuid.uuid1())

    try:
        os.makedirs(full_dir)
        logging.info('created path %s' % full_dir)
    except os.error:
        pass

    global local_files
    local_files.append(full_path)

    with open(full_path, 'wb') as fp:
        while True:
            data = sys.stdin.read(1024)

            if not data:
                break

            fp.write(data)

    logging.info('saved stdin %s' % full_path)
    return full_path

def slugify(s):
    return re.sub(r'[^\w]+', '_', s)

def unlink_files():
    global local_files

    for x in local_files:
        try:
            os.unlink(x)
            logging.info('unlinked %s' % x)
        except:
            pass

if __name__ == '__main__':
    __main__()
