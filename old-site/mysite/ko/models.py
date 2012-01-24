# -*-python-*- Time-stamp: <models.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

import datetime
import re
import scripts.utils as utils

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging import fields

class Part(models.Model):
    content = models.FileField(upload_to='.')
    height = models.IntegerField(default=0)
    name = models.SlugField(unique=True)
    width = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def parents(self):
        return self.plate_set.all()

    def admin_thumbnail(self):
        return u'<img alt="%s" src="%s" />' % (self.name, self.content.url)

    admin_thumbnail.allow_tags = True
    admin_thumbnail.short_description = _('Thumbnail')

class Plate(models.Model):
    class Meta:
        ordering = ['-datetime', 'name']

    GET_ATTRIBUTE_RE = re.compile(r'^get_(\w+)$')

    datetime = models.DateTimeField(default=datetime.datetime.utcnow)
    name = models.SlugField(unique=True)
    parents = models.ManyToManyField('self', related_name='plates', symmetrical=False)
    parts = models.ManyToManyField(Part, through='PlatePart')
    precision = models.IntegerField(blank=True, editable=False, null=True)
    tags = fields.TagField(null=True)

    def __getattr__(self, name):
        m = self.GET_ATTRIBUTE_RE.search(name)

        if not m:
            raise AttributeError("%s has no attribute '%s'" % (self.__class__, name))

        f = lambda: self.get_named_part(*m.groups())

        setattr(self, name, f)
        return f

    def __str__(self):
        return self.name

    @property
    def content_dict(self):
        return dict((p.name, p) for p in self.content_parts)

    @property
    def content_parts(self):
        return self.parts.filter(platepart__name__startswith='__')

    @property
    def datetime_display(self):
        return str(utils.TruncatedDateTime(self.datetime, self.precision))

    @models.permalink
    def get_absolute_url(self):
        return 'ko.views.view_plate', [self.name]

    def get_named_part(self, name):
        try:
            return self.parts.get(platepart__name=name)
        except Part.DoesNotExist:
            pass
        return None

class PlatePart(models.Model):
    class Meta:
        unique_together = ('name', 'plate')

    name = models.SlugField()
    part = models.ForeignKey(Part)
    plate = models.ForeignKey(Plate)

    def __str__(self):
        return "(%s,'%s',%s)" % (self.plate, self.name, self.part)

class Template(models.Model):
    class Meta:
        unique_together = ('name', 'plate')

    name = models.SlugField()
    plate = models.ForeignKey(Plate, related_name='templates')
    text = models.TextField()

    def __str__(self):
        return "(%s,'%s')" % (self.plate, self.name)
