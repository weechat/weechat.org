#
# Copyright (C) 2003-2024 Sébastien Helleu <flashcode@flashtux.org>
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
from django.utils.translation import gettext

from weechat.common.i18n import i18n_autogen

PATTERN_TITLE_VERSION = re.compile('(Version) ([0-9.a-z-]+)$')


class Info(models.Model):
    """A WeeChat info."""
    visible = models.BooleanField(default=False)
    date = models.DateTimeField()
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=256)
    mail = models.EmailField(max_length=256)
    text = models.TextField(blank=True)

    def __str__(self):
        return f'{self.title} ({self.date})'

    def title_i18n(self):
        """Return translated title."""
        match = PATTERN_TITLE_VERSION.match(self.title)
        if match:
            # if the title is "Version x.y.z", translate only "Version"
            return f'{gettext(match.group(1))} {match.group(2)}'
        return gettext(self.title)

    def text_i18n(self):
        """Return translated text."""
        if self.text:
            return gettext(self.text.replace('\r\n', '\n'))
        return ''

    def date_title_url(self):
        """Return date+title to include in URL."""
        text_url = re.sub(' +', '-',
                          re.sub('[^ a-zA-Z0-9.]', ' ', self.title).strip())
        return (f'{self.date.year:0>4}{self.date.month:0>2}{self.date.day:0>2}'
                f'-{text_url}')


def handler_info_saved(sender, **kwargs):
    """Write file _i18n_info.py with infos to translate."""
    # pylint: disable=unused-argument
    strings = []
    for info in Info.objects.filter(visible=1).order_by('-date'):
        match = PATTERN_TITLE_VERSION.match(info.title)
        if match:
            # if the title is "Version x.y.z", translate only "Version"
            strings.append(match.group(1))
        else:
            strings.append(info.title)
        if info.text:
            strings.append(info.text)
    i18n_autogen('news', 'info', strings)


post_save.connect(handler_info_saved, sender=Info)
