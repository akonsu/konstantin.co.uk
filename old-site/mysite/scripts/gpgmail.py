# -*- mode:python; coding:utf-8; -*- Time-stamp: <gpgmail.py - root>
# copyright (c) konstantin.co.uk. all rights reserved.

__all__ = ['filter_parts', 'flatten', 'signed_parts',]

import os
import re
import tempfile

from contextlib import closing
from cStringIO import StringIO
from email.generator import Generator
from email.message import Message
from subprocess import PIPE, Popen

class Result(object):
    def __init__(self, fp):
        STATUS_RE = re.compile(r'^\s*\[GNUPG:\]\s*(\w+)((?:\s+[^\s]+)*)\s*$')

        self.fingerprint = None
        self.is_valid = False
        self.key_id = None
        self.username = None

        for s in fp:
            m = STATUS_RE.match(s)

            if m:
                status, tail = m.groups()
                if status == 'GOODSIG':
                    self.is_valid = True
                    self.key_id, self.username = tail.split(None, 1)

                elif status == 'VALIDSIG':
                    self.fingerprint = tail.split(None, 1)[0]

    def __nonzero__(self):
        return self.is_valid

    __bool__ = __nonzero__

def _verify(message, signature=None):
    try:
        message_fname = ''
        signature_fname = ''

        if signature:
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                fp.write(signature.get_payload())
                signature_fname = fp.name

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(flatten(message) if isinstance(message, Message) else message)
            message_fname = fp.name

        command = ['gpg --status-fd 2 --no-tty --verify', signature_fname, message_fname]
        stdout, stderr = Popen(' '.join(command), shell=True, stdout=PIPE, stderr=PIPE).communicate()

        with closing(StringIO(stderr)) as fp:
            return Result(fp)

    finally:
        if message_fname:
            os.unlink(message_fname)

        if signature_fname:
            os.unlink(signature_fname)

def filter_parts(m, f):
    'Iterate over messages that satisfy predicate.'
    for x in m.walk():
        if f(x):
            yield x

def flatten(message):
    'Return raw string representation of message.'
    with closing(StringIO()) as s:
        g = Generator(s, mangle_from_=False, maxheaderlen=0)

        g.flatten(message)
        return s.getvalue()

def signed_parts(message):
    'Iterate over signed parts of message yielding GPG verification status and signed contents.'
    ARMOR_RE = re.compile(r'^-+BEGIN PGP SIGNED MESSAGE-+\n(?:.*\n)+\n((?:.*\n)+)-+BEGIN PGP SIGNATURE-+\n(?:.*\n)+-+END PGP SIGNATURE-+\s*$')

    f = lambda m: m.is_multipart() and m.get_content_type() == 'multipart/signed' or not m.is_multipart() and m.get_content_maintype() == 'text'

    for part in filter_parts(message, f):
        if part.is_multipart():
            try:
                signed_part, signature=part.get_payload()

                yield _verify(signed_part, signature), signed_part

            except ValueError:
                pass

        else:
            payload = part.get_payload(decode=True)
            m = ARMOR_RE.match(payload)

            if m:
                yield _verify(payload), m.group(1)
