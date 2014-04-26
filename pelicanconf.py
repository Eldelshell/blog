#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eldelshell'
SITENAME = u'Eldelshell Blog'
SITEURL = 'http://www.eldelshell.com'
THEME = "theme/"
LOCALE = 'en_US.UTF-8'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

LINKS =  ()
SOCIAL = (('Twitter', 'http://twitter.com/Eldelshell'),
          ('Google+', 'https://plus.google.com/+AlejandroAyuso?rel=author'),
          ('StackExchange', 'http://stackoverflow.com/users/48869/eldelshell'),
          ('LinkedIn', 'http://es.linkedin.com/in/alejandroayuso/'),
          ('RSS', 'http://www.eldelshell.com/feeds/all.atom.xml'))

DEFAULT_PAGINATION = 10
RELATIVE_URLS = True
FAVICON = 'static/images/favicon.ico'
TWITTER_USERNAME = 'Eldelshell'
BOOTSTRAP_THEME = 'flatly'
GOOGLE_PLUS_ID = '+AlejandroAyuso'
CC_LICENSE = "CC-BY"
TAG_CLOUD_MAX_ITEMS = 20
STACK_OVERFLOW = False

SITESUBTITLE = 'Software development and architecture blog'

# SEO
SEO_DESCRIPTION = 'Software and technology blog' 
SEO_KEYWORDS = 'eldelshell, software, technology, java, linux, web, development, alejandro, ayuso, blog, personal'
SITEMAP_SAVE_AS = 'sitemap.xml'
DIRECT_TEMPLATES = ('index', 'archives', 'sitemap')
USE_TWITTER_CARDS = True

# Hide categories in top bar
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
