# -*- mode:python; coding:utf-8; -*- Time-stamp: <views.py - root>

import smtplib

from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views import generic
from ko import forms
from mysite import settings

class ContactFormView(generic.edit.FormView):
    form_class = forms.ContactForm
    success_url = lazy(reverse, str)('contact')
    template_name = 'contact.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        name = form.cleaned_data['name']

        try:
            send_mail('email from visitor %s' % name, message, email, ('akonsu@gmail.com',) )
            messages.success(self.request, 'Your e-mail has been sent. If your message needs a response, I will get back to you as soon as I can. Best regards and thanks!')

        except smtplib.SMTPException:
            messages.error(self.request, 'The server encountered an error while sending your e-mail. Please contact me at root@konstantin.co.uk directly. Best regards and thanks!')

        return super(ContactFormView, self).form_valid(form)

class ProjectsView(generic.TemplateView):
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsView, self).get_context_data(**kwargs)

        context['projects'] = [{'description': (u'<a href="http://www.eaglectg.com/" target="_blank">eaglectg.com</a><br>'
                                                u'**2011**'
                                                u'\n\n'
                                                u'Eagle Consulting Technology Group are a young Seattle based technology consulting agency.\n'
                                                u'Eagle Consulting asked me to redesign their existing website to better define their identity and brand name.\n'
                                                u'They also needed an online job board to be able to post job advertisements on behalf of their customers.'
                                                u'\n\n'
                                                u'The site is built using Python, Django, and HTML5.<br>'
                                                u'The logo is created by <a href="http://lauravdesign.com/" target="_blank">Laura Vasyutynska</a>.'),
                                'screenshot': '%simages/eaglectg_com.jpg' % settings.STATIC_URL,
                                },
                               {'description': (u'<a href="http://konstantin.co.uk/" target="_blank">konstantin.co.uk</a> (this site)<br>'
                                                u'**2011**'
                                                u'\n\n'
                                                u'This is my online portfolio that features both client based and self-initiated projects for the web, as well as visual art.'
                                                u'\n\n'
                                                u'The site is written in Python using Django and HTML5.'),
                                'screenshot': '%simages/konstantin_co_uk.jpg' % settings.STATIC_URL,
                                },
                               ]

        return context
