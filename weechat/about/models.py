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
# along with WeeChat.org.  If not, see <http://www.gnu.org/licenses/>.
#

"""Models for "about" menu."""

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy, ugettext, ugettext_noop

from weechat.common.i18n import i18n_autogen
from weechat.common.templatetags.localdate import localdate
from weechat.common.tracker import commits_links, tracker_links

CVE_URL = ('<a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=%(cve)s" '
           'target="_blank" rel="noopener">%(cve)s</a>')

SECURITY_SEVERITIES = (
    # Translators: this is a severity level for a security vulnerability
    (0, ugettext_noop('low')),
    # Translators: this is a severity level for a security vulnerability
    (1, ugettext_noop('medium')),
    # Translators: this is a severity level for a security vulnerability
    (2, ugettext_noop('high')),
    # Translators: this is a severity level for a security vulnerability
    (3, ugettext_noop('critical')),
)


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
        return gettext_lazy(self.text.replace('\r\n', '\n'))

    class Meta:
        """Meta class for KeyDate."""
        ordering = ['-date']


def handler_keydate_saved(sender, **kwargs):
    """Write file _i18n_keydates.py with key dates to translate."""
    strings = []
    for keydate in Keydate.objects.order_by('-date'):
        strings.append(keydate.text)
    i18n_autogen('about', 'keydates', strings)


post_save.connect(handler_keydate_saved, sender=Keydate)


class Security(models.Model):
    """A security vulnerability in WeeChat."""
    visible = models.BooleanField(default=True)
    date = models.DateTimeField()
    external = models.CharField(max_length=1024, blank=True)
    tracker = models.CharField(max_length=64, blank=True)
    severity = models.IntegerField(default=0, choices=SECURITY_SEVERITIES)
    affected = models.CharField(max_length=64, blank=True)
    fixed = models.CharField(max_length=32, blank=True)
    release_date = models.DateField(blank=True, null=True)
    commits = models.CharField(max_length=1024, blank=True)
    description = models.TextField()
    workaround = models.TextField(blank=True)

    def __str__(self):
        return '%s, %s, %s, %s / %s, %s, %s' % (
            self.external, self.tracker, self.severity,
            self.affected, self.fixed, self.release_date,
            self.description)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def date_l10n(self):
        """Return the date formatted with localized date format."""
        return localdate(self.date)

    def external_links(self):
        """Return URL to CVE (or "external" as-is if it's not a CVE)."""
        if self.external.startswith('CVE'):
            return CVE_URL % {'cve': self.external}
        return self.external

    def url_tracker(self):
        """Return URL with links to tracker items."""
        return tracker_links(self.tracker)

    def severity_i18n(self):
        """Return translated severity."""
        text = dict(SECURITY_SEVERITIES).get(self.severity, '')
        if text:
            return ugettext(text)
        return ''

    def css_class(self):
        """Return the CSS class for the severity."""
        css_class = {
            0: 'light',
            1: 'secondary',
            2: 'warning',
            3: 'danger',
        }
        return css_class[self.severity]

    def affected_html(self):
        """Return affected versions for display in HTML."""
        return self.affected.replace(',', ' &rarr; ')

    def release_date_l10n(self):
        """Return the release date formatted with localized date format."""
        return localdate(self.release_date)

    def url_commits(self):
        """Return URL with links to commits."""
        return commits_links(self.commits)

    def description_i18n(self):
        """Return the translated description."""
        if self.description:
            return gettext_lazy(self.description.replace('\r\n', '\n'))
        return ''

    def workaround_i18n(self):
        """Return translated workaround."""
        if self.workaround:
            return gettext_lazy(self.workaround.replace('\r\n', '\n'))
        return ''

    class Meta:
        ordering = ['-date']


def handler_security_saved(sender, **kwargs):
    """Write file _i18n_security.py with security issues to translate."""
    strings = []
    for security in Security.objects.filter(visible=1).order_by('-date'):
        if security.description:
            strings.append(security.description)
        if security.workaround:
            strings.append(security.workaround)
    i18n_autogen('about', 'security', strings)


post_save.connect(handler_security_saved, sender=Security)


class Sponsor(models.Model):
    """A WeeChat sponsor."""
    name = models.CharField(max_length=64)
    date = models.DateField()
    site = models.CharField(max_length=512, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.IntegerField(default=1)
    comment = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        str_num = ' (#%d)' % self.number if self.number > 1 else ''
        return '%s%s, %s, %.02f Eur' % (self.name, str_num, self.date,
                                        self.amount)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def date_l10n(self):
        """Return the sponsor date formatted with localized date format."""
        return localdate(self.date)
