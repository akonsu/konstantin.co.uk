# -*- mode:python; coding:utf-8; -*- Time-stamp: <utils.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

__all__ = ['AdminMailingHandler', 'call_on_error', 'get_email_datetime', 'TruncatedDateTime',]

import contextlib
import datetime
import logging.handlers
import re
import sys

from django.core.mail import mail_admins
from email.utils import mktime_tz, parsedate_tz

class AdminMailingHandler(logging.handlers.BufferingHandler):
    'Logging handler that supports sending logging messages to email address.'
    def __init__(self, capacity=1024):
        logging.handlers.BufferingHandler.__init__(self, capacity)

        self.subject = ''

    def flush(self):
        if len(self.buffer) > 0:
            try:
                mail_admins(self.subject, reduce(lambda s, x: s + self.format(x) + '\r\n', self.buffer, ''))

            except:
                self.handleError(None)

            self.buffer = []

@contextlib.contextmanager
def call_on_error(f):
    'Call callable if exception is thrown.'
    try:
        yield

    except:
        type, value, traceback = sys.exc_info()

        try:
            try:
                if callable(f):
                    f()
            except:
                pass
            raise type, value, traceback

        finally:
            del type, value, traceback

def get_email_datetime(message):
    'Retrieve date and time from e-mail message.'
    timestamp = mktime_tz(parsedate_tz(message['date']))

    return datetime.datetime.utcfromtimestamp(timestamp)

class TruncatedDateTime(object):
    'Date and time truncated using given precision.'

    # YYYY[-MM[-DD[ HH:MM[:ss]]]]
    SYNTAX_RE = re.compile(r'^\s*(\d{4})(?:-(\d{1,2})(?:-(\d{1,2})(?:\s+(\d{2}):(\d{2})(?::(\d{2}))?)?)?)?\s*$')

    def __init__(self, value, precision=None):
        if isinstance(value, datetime.datetime):
            self.precision = precision
            self.value = value

        elif isinstance(value, datetime.date):
            self.precision = 3
            self.value = datetime.datetime(value.year, value.month, value.day)

        else:
            m = TruncatedDateTime.SYNTAX_RE.search(str(value))

            if not m:
                raise ValueError(value)

            members = map(int, filter(None, m.groups()))

            kwargs = dict(year=datetime.MINYEAR, month=1, day=1)
            kwargs.update(zip(('year', 'month', 'day', 'hour', 'minute', 'second'), members))

            self.precision = len(members)
            self.value = datetime.datetime(**kwargs)

    def __str__(self):
        FORMATS = ('%Y', '%b %Y', '%Y-%m-%d', '%Y-%m-%d %H:00', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S')
        return self.value.strftime(FORMATS[max(0, min(self.precision, len(FORMATS))) - 1])
