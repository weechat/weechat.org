#
# Copyright (C) 2003-2021 Sébastien Helleu <flashcode@flashtux.org>
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
# along with WeeChat.org.  If not, see <https://www.gnu.org/licenses/>.
#

# Django settings for weechat project.

"""weechat.org settings."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Override these values in settings_local.py for production
DEBUG = True
SECRET_KEY = 'replace-me'
ALLOWED_HOSTS = []
ADMINS = []
MANAGERS = []
THEMES_MAILTO = []

SITE_ID = 1

TIME_ZONE = 'Europe/Paris'

LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_L10N = False

gettext = lambda s: s  # noqa: E731  pylint: disable=C0103
LANGUAGES = (
    ('en', gettext('English')),
    ('fr', gettext('French')),
    ('de', gettext('German')),
    ('it', gettext('Italian')),
    ('pl', gettext('Polish')),
    ('pt-br', gettext('Portuguese (Brazil)')),
    ('ja', gettext('Japanese')),
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

# Themes
THEMES = (
    'auto',
    'dark',
    'light',
)

# Translators: this is a date format, see: http://www.php.net/date
# Translators: (note: the result string must be short, use abbreviation
# Translators: for month if possible)
DATE_FORMAT = gettext('M j, Y')

# Translators: this is a date/time format, see: http://www.php.net/date
# Translators: (note: the result string must be short, use abbreviation
# Translators: for month if possible)
DATETIME_FORMAT = gettext('M j, Y H:i')

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'

FILES_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'files'))
FILES_URL = '/files/'

STATIC_URL = '/static/'

REPO_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'repo'))

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'weechat.common',
    'weechat.news',
    'weechat.about',
    'weechat.doc',
    'weechat.download',
    'weechat.debian',
    'weechat.scripts',
    'weechat.themes',
    'weechat.dev',
]

ROOT_URLCONF = 'weechat.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'weechat.middleware.ThemeMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'weechat.context_processors.theme',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'weechat.db',
    },
}

ADMIN_PAGE = 'admin'

# read settings_local.py (optional file)
try:
    # pylint: disable=wildcard-import,unused-wildcard-import
    from weechat.settings_local import *  # noqa: F401,F403
except ImportError:
    pass
