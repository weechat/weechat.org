# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2014 Sébastien Helleu <flashcode@flashtux.org>
#
# This file is part of WeeChat.org.
#
# WeeChat.org is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# WeeChat.org is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WeeChat.org.  If not, see <http://www.gnu.org/licenses/>.
#

# Django settings for weechat project.

from os import path

DEBUG = False
TEMPLATE_DEBUG = DEBUG

BASE_DIR = path.dirname(path.abspath(__file__))

ADMINS = ()  # set it in settings_local.py
MANAGERS = ADMINS

DATABASES = {}  # set it in settings_local.py

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
    ('fr', ugettext('French')),
    ('de', ugettext('German')),
    ('it', ugettext('Italian')),
    ('pl', ugettext('Polish')),
    ('pt-br', ugettext('Portuguese (Brazil)')),
    ('ja', ugettext('Japanese')),
)
LANGUAGES_LOCALES = {
    'en': 'en_US',
    'fr': 'fr_FR',
    'de': 'de_DE',
    'it': 'it_IT',
    'pl': 'pl_PL',
    'pt-br': 'pt_BR',
    'ja': 'ja_JP',
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.normpath(path.join(BASE_DIR, '..', 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Page for admin (can be overriden in settings_local.py)
ADMIN_PAGE = 'admin'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media_admin/'  # for Django <= 1.3

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

FILES_ROOT = path.normpath(path.join(BASE_DIR, '..', 'files'))

REPO_DIR = path.normpath(path.join(BASE_DIR, '..', 'repo'))

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''  # set it in settings_local.py

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'weechat.urls'

TEMPLATE_DIRS = (
    path.join(BASE_DIR, 'templates'),
)

FIXTURE_DIRS = (
    path.join(BASE_DIR, 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'weechat.common',
    'weechat.news',
    'weechat.about',
    'weechat.doc',
    'weechat.download',
    'weechat.debian',
    'weechat.plugins',
    'weechat.themes',
    'weechat.dev',
)

LOCALE_PATHS = (
    path.join(BASE_DIR, 'locale'),
)

ugettext = lambda s: s
# Translators: this is a date format, see: http://uk3.php.net/manual/en/function.date.php (note: the result string must be short, use abbreviation for month if possible)
DATE_FORMAT = ugettext('M j, Y')

# read settings_local.py
try:
    from settings_local import *
except ImportError:
    from warnings import warn
    warn('File "settings_local.py" not found, using default settings')
