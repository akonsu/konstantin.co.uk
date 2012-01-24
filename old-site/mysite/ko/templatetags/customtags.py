# -*-python-*- Time-stamp: <customtags.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

import re

from django.core.exceptions import ObjectDoesNotExist
from django.template import resolve_variable
from django.template import Library, Node, Template, TemplateSyntaxError, VariableDoesNotExist

register = Library()

class PlateNode(Node):
    def __init__(self, plate, template_name):
        self.plate = plate
        self.template_name = template_name

    def render(self, context):
        def _mk_template(plate, name):
            if name:
                try:
                    return Template(plate.templates.get(name=name).text)

                except ObjectDoesNotExist:
                    pass

            return None

        result = ''

        try:
            plate = resolve_variable(self.plate, context)
            context.push()
            context['self'] = plate
            template = _mk_template(plate, self.template_name) or _mk_template(plate, 'default')
            result = template.render(context)
            context.pop()

        except (AttributeError, IndexError, KeyError, VariableDoesNotExist):
            pass

        return result

PLATE_TAG_RE = re.compile(r'^\s*plate\s+(\S+)(?:\s*,\s*template\s*=\s*(\S+))?\s*$')

@register.inclusion_tag('paginator.html', takes_context=True)
def pages(context):
    page_obj = context.get('page_obj')
    return {'digg_page_range': page_obj.paginator.digg_page_range(page_obj),
            'page_obj': page_obj,
            'single_page': page_obj.paginator.num_pages < 2} if page_obj else {'single_page': True}

@register.tag
def plate(parser, token):
    m = PLATE_TAG_RE.search(token.contents)
    if not m:
        raise TemplateSyntaxError, 'invalid syntax'
    return PlateNode(*m.groups())
