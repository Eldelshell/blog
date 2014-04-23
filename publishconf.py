#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# SITEURL = 'http://eldelshell.github.io/'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None

DELETE_OUTPUT_DIRECTORY = True

# FILES_TO_COPY = ('extra/robots.txt', 'robots.txt')

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
GOOGLE_ANALYTICS_OLD = 'UA-50208536-1'
# GOOGLE_ANALYTICS = 'UA-50208536-1'
# GOOGLE_ANALYTICS_SITE = 'eldelshell.github.io'
