# -*- mode:python; coding:utf-8; -*- Time-stamp: <forms.py - root>

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label=u'Your name', max_length=128)
    email = forms.EmailField(label=u'Your e-mail')
    message = forms.CharField(label = u'Message', widget = forms.Textarea())
