#!/usr/local/var/pyenv/shims/python
# -*- coding: utf-8 -*-

import os
import sys

import time
from datetime import datetime
from email.utils import parsedate

filter_user = os.environ.get('SWEETSHOP_EMAIL', 'wangwenpei@nextoa.com').split(
    ',')

for line in sys.stdin:
    values = line.strip().split(";")

    user = "-1"
    datetime_string = "-1"

    t = parsedate(values[1])
    date_time_obj = datetime.fromtimestamp(time.mktime(t))

    if values[0] not in filter_user:
        continue

    print("%s^%s" % (
        values[0],
        date_time_obj
    ))
