# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Models for news."""

import re

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext

from weechat.common.i18n import i18n_autogen

PATTERN_TITLE_VERSION = re.compile('(Version) ([0-9.a-z-]+)$')


class Info(models.Model):
    """A WeeChat info."""
    id = models.AutoField(primary_key=True)
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
