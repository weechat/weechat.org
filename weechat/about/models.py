# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2020 Sébastien Helleu <flashcode@flashtux.org>
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

"""Models for "about" menu."""

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext, ugettext_lazy

from weechat.common.i18n import i18n_autogen
from weechat.common.templatetags.localdate import localdate


SPONSOR_TYPE_CHOICES = (
    (0,
     # Translators: context: Individual / Association / Company
     ugettext_lazy('Individual')),
    (1,
     # Translators: context: Individual / Association / Company
     ugettext_lazy('Association')),
    (2,
     # Translators: context: Individual / Association / Company
     ugettext_lazy('Company')),
)
SPONSOR_TYPE_SVG = {
    0: 'person',
    1: 'persons',
    2: 'briefcase',
}


class Screenshot(models.Model):
    """A WeeChat screenshot."""
    app = models.CharField(max_length=256)
    filename = models.CharField(max_length=256)
    comment = models.TextField(blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return '%s: %s (%d)' % (self.app, self.filename, self.priority)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    class Meta:
        """Meta class for ScreenShot."""
        ordering = ['priority']


class Keydate(models.Model):
    """A WeeChat key date."""
    date = models.DateField()
    version = models.TextField(max_length=32)
    text = models.TextField()

    def __str__(self):
        str_version = ('%s: ' % self.version) if self.version else ''
        return '%s - %s%s' % (self.date, str_version, self.text)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def text_i18n(self):
        """Return translated key date."""
        return ugettext(self.text.replace('\r\n', '\n'))

    class Meta:
        """Meta class for KeyDate."""
        ordering = ['-date']


def handler_keydate_saved(sender, **kwargs):
    """Write file _i18n_keydates.py with key dates to translate."""
    # pylint: disable=unused-argument
    strings = []
    for keydate in Keydate.objects.order_by('-date'):
        strings.append(keydate.text)
    i18n_autogen('about', 'keydates', strings)


post_save.connect(handler_keydate_saved, sender=Keydate)


class Sponsor(models.Model):
    """A WeeChat sponsor."""
    sponsortype = models.IntegerField(choices=SPONSOR_TYPE_CHOICES, default=0)
    name = models.CharField(max_length=64)
    date = models.DateField()
    site = models.CharField(max_length=512, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.IntegerField(default=1)
    comment = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        str_num = ' (#%d)' % self.number if self.number > 1 else ''
        return '%s%s, %s, %s, %.02f Eur' % (self.name,
                                            str_num,
                                            self.sponsortype_i18n(),
                                            self.date,
                                            self.amount)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def date_l10n(self):
        """Return the sponsor date formatted with localized date format."""
        return localdate(self.date)

    def sponsortype_i18n(self):
        """Return the translated sponsor type."""
        return ugettext(dict(SPONSOR_TYPE_CHOICES)[self.sponsortype])

    def sponsortype_svg(self):
        """Return the name of SVG for the sponsor type."""
        return SPONSOR_TYPE_SVG[self.sponsortype]
