# -*-python-*- Time-stamp: <admin.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

from django.contrib import admin
from ko.models import *

class PlateAdmin(admin.ModelAdmin):
    pass

class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'admin_thumbnail')

admin.site.register(Plate, PlateAdmin)
admin.site.register(PlatePart)
admin.site.register(Part, PartAdmin)
admin.site.register(Template)
