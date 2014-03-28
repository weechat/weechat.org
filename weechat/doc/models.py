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

from django.db import models
from django.utils.translation import ugettext, ugettext_noop


class Language(models.Model):
    LANG_I18N = {
        'cs': ugettext_noop('Czech'),
        'de': ugettext_noop('German'),
        'en': ugettext_noop('English'),
        'es': ugettext_noop('Spanish'),
        'fr': ugettext_noop('French'),
        'hu': ugettext_noop('Hungarian'),
        'it': ugettext_noop('Italian'),
        'ja': ugettext_noop('Japanese'),
        'pl': ugettext_noop('Polish'),
        'pt_BR': ugettext_noop('Portuguese (Brazil)'),
        'ru': ugettext_noop('Russian'),
        'tr': ugettext_noop('Turkish'),
    }
    lang = models.CharField(max_length=8, primary_key=True)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s (%d)' % (self.lang, self.priority)

    def lang_i18n(self):
        return ugettext(self.LANG_I18N[self.lang])

    class Meta:
        ordering = ['priority']


class Version(models.Model):
    version = models.CharField(max_length=32, primary_key=True)
    priority = models.IntegerField(default=0)
    directory = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.version

    class Meta:
        ordering = ['priority']


class Doc(models.Model):
    NAME_I18N = {
        'faq': ugettext_noop('FAQ'),
        'user': ugettext_noop('User\'s guide'),
        'plugin_api': ugettext_noop('Plugin API reference'),
        'scripting': ugettext_noop('Scripting guide'),
        'quickstart': ugettext_noop('Quick Start guide'),
        'tester': ugettext_noop('Tester\'s guide'),
        'dev': ugettext_noop('Developer\'s guide'),
        'relay_protocol': ugettext_noop('Relay protocol'),
    }
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=64)
    devel = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s (%s, %d)' % (self.name, self.version, self.priority)

    def name_i18n(self):
        return ugettext(self.NAME_I18N[self.name])

    class Meta:
        ordering = ['priority']
