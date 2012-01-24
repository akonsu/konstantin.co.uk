# -*- mode:python; coding:utf-8; -*- Time-stamp: <customtags.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

import re

from django import template

register = template.Library()

EVALUATE_TAG_RE = re.compile(r'^\s*evaluate\s+(\S+)\s*$')

class EvaluateNode(template.Node):
    def __init__(self, variable):
        self.variable = template.Variable(variable)

    def render(self, context):
        try:
            content = self.variable.resolve(context)
            t = template.Template(content)
            return t.render(context)
        except template.TemplateSyntaxError, template.VariableDoesNotExist:
            return 'Error rendering', self.variable

@register.tag
def evaluate(parser, token):
    m = EVALUATE_TAG_RE.search(token.contents)
    if not m :
        raise TemplateSyntaxError, 'invalid syntax'
    return EvaluateNode(*m.groups())
