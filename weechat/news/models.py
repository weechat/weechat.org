# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2018 Sébastien Helleu <flashcode@flashtux.org>
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

"""Models for news."""

import re

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext

from weechat.common.i18n import i18n_autogen
from weechat.common.templatetags.localdate import localdate

PATTERN_TITLE_VERSION = re.compile('(Version) ([0-9.a-z-]*)$')


class Info(models.Model):
    """A WeeChat info."""
    visible = models.BooleanField(default=False)
    date = models.DateTimeField()
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=256)
    mail = models.EmailField(max_length=256)
    text = models.TextField(blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.date)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def date_l10n(self):
        """Return the info date formatted with localized date format."""
        return localdate(self.date)

    def title_i18n(self):
        """Return translated title."""
        match = PATTERN_TITLE_VERSION.match(self.title)
        if match:
            # if the title is "Version x.y.z", translate only "Version"
            return '%s %s' % (ugettext(match.group(1)), match.group(2))
        else:
            return ugettext(self.title)

    def text_i18n(self):
        """Return translated text."""
        if self.text:
            return ugettext(self.text.replace('\r\n', '\n'))
        return ''

    def date_title_url(self):
        """Return date+title to include in URL."""
        return '%04d%02d%02d-%s' % (self.date.year, self.date.month,
                                    self.date.day,
                                    re.sub(' +', '-',
                                           re.sub('[^ a-zA-Z0-9.]', ' ',
                                                  self.title).strip()))


def handler_info_saved(sender, **kwargs):
    strings = []
    for info in Info.objects.filter(visible=1).order_by('-date'):
        m = PATTERN_TITLE_VERSION.match(info.title)
        if m:
            # if the title is "Version x.y.z", translate only "Version"
            strings.append(m.group(1))
        else:
            strings.append(info.title)
        if info.text:
            strings.append(info.text)
    i18n_autogen('news', 'info', strings)


post_save.connect(handler_info_saved, sender=Info)
