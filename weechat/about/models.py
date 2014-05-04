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
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy

from weechat.common.i18n import i18n_autogen
from weechat.common.templatetags.localdate import localdate


class Screenshot(models.Model):
    directory = models.CharField(max_length=256)
    filename = models.CharField(max_length=256)
    comment = models.TextField(blank=True)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s/%s (%d)' % (self.directory, self.filename, self.priority)

    class Meta:
        ordering = ['priority']


class Keydate(models.Model):
    date = models.DateField()
    version = models.TextField(max_length=32)
    text = models.TextField()

    def __unicode__(self):
        return '%s - %s' % (self.date, self.text)

    def text_i18n(self):
        return gettext_lazy(self.text.replace('\r\n', '\n'))

    class Meta:
        ordering = ['-date']


def handler_keydate_saved(sender, **kwargs):
    strings = []
    for keydate in Keydate.objects.order_by('-date'):
        strings.append(keydate.text)
    i18n_autogen('about', 'keydates', strings)

post_save.connect(handler_keydate_saved, sender=Keydate)


class Sponsor(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField()
    site = models.CharField(max_length=512, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.IntegerField(default=1)
    comment = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return '%s, %s, %.02f Eur' % (self.name, self.date, self.amount)

    def date_l10n(self):
        return localdate(self.date)
