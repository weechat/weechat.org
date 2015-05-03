# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2015 Sébastien Helleu <flashcode@flashtux.org>
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

"""Models for "download" menu."""

from datetime import datetime
from hashlib import sha1
from os import path

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy, ugettext, ugettext_noop

from weechat.common.i18n import i18n_autogen
from weechat.common.path import files_path_join
from weechat.common.tracker import commits_links, tracker_links
from weechat.common.templatetags.localdate import localdate

CVE_URL = ('<a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=%(cve)s" '
           'target="_blank">%(cve)s</a>')


class Release(models.Model):
    """A WeeChat release."""
    version = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=64, blank=True)
    date = models.DateField(blank=True, null=True)
    securityfix = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.version, self.date)

    def date_l10n(self):
        """Return the release date formatted with localized date format."""
        return localdate(self.date)

    class Meta:
        ordering = ['-date']


class Type(models.Model):
    """A type of package (source, debian, ...)."""
    type = models.CharField(max_length=64, primary_key=True)
    priority = models.IntegerField(default=0)
    description = models.CharField(max_length=256)
    icon = models.CharField(max_length=64, blank=True)
    directory = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return '%s - %s (%d)' % (self.type, self.description, self.priority)

    def htmldir(self):
        """Return the HTML directory for the type of package."""
        if self.directory != '':
            return '/%s' % self.directory
        return ''

    class Meta:
        ordering = ['priority']


class Package(models.Model):
    """A WeeChat package."""
    version = models.ForeignKey(Release)
    type = models.ForeignKey(Type)
    filename = models.CharField(max_length=512, blank=True)
    sha1sum = models.CharField(max_length=128, blank=True)
    display_time = models.BooleanField(default=False)
    directory = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=512, blank=True)
    text = models.CharField(max_length=512, blank=True)

    def __unicode__(self):
        if self.filename != '':
            string = self.filename
        elif self.directory != '':
            string = self.directory
        elif self.url != '':
            string = self.url
        else:
            string = self.text
        return '%s-%s, %s' % (self.version.version, self.type.type, string)

    def fullname(self):
        """Return the path for package."""
        if self.filename:
            return files_path_join(self.type.directory, self.filename)
        if self.directory:
            return files_path_join(self.directory)
        return ''

    def fullname_gpg_sig(self):
        """Return the path for the GPG signature."""
        return self.fullname() + '.asc'

    def has_gpg_sig(self):
        """Checks if the package has a GPG signature."""
        return path.isfile(self.fullname_gpg_sig())

    def exists(self):
        """Checks if the package exists (on disk)."""
        return path.exists(self.fullname())

    def filesize(self):
        """Return the size of package, in bytes (as string)."""
        try:
            return str(path.getsize(self.fullname()))
        except:
            return ''

    def filedate(self):
        """Return the package date/time."""
        try:
            return datetime.fromtimestamp(path.getmtime(self.fullname()))
        except:
            return ''

    class Meta:
        ordering = ['version', '-type__priority']


def handler_package_saved(sender, **kwargs):
    """Compute sha1sum of file."""
    try:
        package = kwargs['instance']
        if package.filename:
            with open(package.fullname(), 'rb') as _file:
                package.sha1sum = sha1(_file.read()).hexdigest()
    except:
        pass

pre_save.connect(handler_package_saved, sender=Package)

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

    def __unicode__(self):
        return '%s, %s, %s, %s / %s, %s, %s' % (
            self.external, self.tracker, self.severity,
            self.affected, self.fixed, self.release_date,
            self.description)

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
    i18n_autogen('download', 'security', strings)

post_save.connect(handler_security_saved, sender=Security)


class ReleaseTodo(models.Model):
    """A 'to do' item for a release."""
    description = models.CharField(max_length=1024)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s (%d)' % (self.description, self.priority)

    class Meta:
        ordering = ['priority']


class ReleaseProgress(models.Model):
    """The progress for the next release."""
    version = models.ForeignKey(Release, primary_key=True)
    done = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s, %d' % (self.version, self.done)

    class Meta:
        verbose_name_plural = 'release progress'
