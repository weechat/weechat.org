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

"""Models for "download" menu."""

from datetime import datetime
from hashlib import sha1, sha512
import os
import pytz

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from weechat.common.path import files_path_join
from weechat.common.templatetags.localdate import localdate


class Release(models.Model):
    """A WeeChat release."""
    version = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=64, blank=True)
    date = models.DateField(blank=True, null=True)
    security_issues_fixed = models.IntegerField(default=0)
    securityfix = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return '%s (%s)%s%s' % (
            self.version,
            self.date,
            (', %d SECURITY FIX' % self.security_issues_fixed
             if self.security_issues_fixed > 0 else ''),
            (', fix in: %s' % ', '.join(self.securityfix.split(','))
             if self.securityfix else ''),
        )

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def date_l10n(self):
        """Return the release date formatted with localized date format."""
        return localdate(self.date)

    def security_fixed_versions(self):
        """Return the list of versions fixing security issues."""
        return self.securityfix.split(',')

    class Meta:
        ordering = ['-date']


class Type(models.Model):
    """A type of package (source, debian, etc.)."""
    type = models.CharField(max_length=64, primary_key=True)
    priority = models.IntegerField(default=0)
    description = models.CharField(max_length=256)
    icon = models.CharField(max_length=64, blank=True)
    directory = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return '%s - %s (%d)' % (self.type, self.description, self.priority)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def htmldir(self):
        """Return the HTML directory for the type of package."""
        if self.directory != '':
            return '/%s' % self.directory
        return ''

    class Meta:
        ordering = ['priority']


class Package(models.Model):
    """A WeeChat package."""
    version = models.ForeignKey(Release, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    filename = models.CharField(max_length=512, blank=True)
    sha1sum = models.CharField(max_length=128, blank=True)
    sha512sum = models.CharField(max_length=128, blank=True)
    display_time = models.BooleanField(default=False)
    directory = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=512, blank=True)
    text = models.CharField(max_length=512, blank=True)

    def __str__(self):
        if self.filename != '':
            string = self.filename
        elif self.directory != '':
            string = self.directory
        elif self.url != '':
            string = self.url
        else:
            string = self.text
        return '%s-%s, %s' % (self.version.version, self.type.type, string)

    def __unicode__(self):  # python 2.x
        return self.__str__()

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

    def has_checksum(self):
        """Checks if the package has a checksum."""
        return any([self.sha512sum, self.sha1sum])

    def checksum_type(self):
        """Return the type of package checksum."""
        if self.sha512sum:
            return 'sha512'
        if self.sha1sum:
            return 'sha1'
        return ''

    def checksum(self):
        """Return the package checksum."""
        if self.sha512sum:
            return self.sha512sum
        if self.sha1sum:
            return self.sha1sum
        return ''

    def has_gpg_sig(self):
        """Checks if the package has a GPG signature."""
        return os.path.isfile(self.fullname_gpg_sig())

    def exists(self):
        """Checks if the package exists (on disk)."""
        return os.path.exists(self.fullname())

    def filesize(self):
        """Return the size of package, in bytes (as string)."""
        try:
            return str(os.path.getsize(self.fullname()))
        except:  # noqa: E722
            return ''

    def filedate(self):
        """Return the package date/time."""
        try:
            timezone = pytz.timezone(settings.TIME_ZONE)
            return datetime.fromtimestamp(os.path.getmtime(self.fullname()),
                                          tz=timezone)
        except:  # noqa: E722
            return ''

    class Meta:
        ordering = ['version', '-type__priority']


def handler_package_saved(sender, **kwargs):
    """Compute SHA-1 and SHA-512 of file."""
    try:
        package = kwargs['instance']
        if package.filename and package.version.version != 'devel':
            with open(package.fullname(), 'rb') as _file:
                package.sha1sum = sha1(_file.read()).hexdigest()
            with open(package.fullname(), 'rb') as _file:
                package.sha512sum = sha512(_file.read()).hexdigest()
    except:  # noqa: E722
        pass


pre_save.connect(handler_package_saved, sender=Package)


class ReleaseTodo(models.Model):
    """A 'to do' item for a release."""
    description = models.CharField(max_length=1024)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return '%s (%d)' % (self.description, self.priority)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    class Meta:
        ordering = ['priority']


class ReleaseProgress(models.Model):
    """The progress for the next release."""
    version = models.OneToOneField(Release, primary_key=True,
                                   on_delete=models.CASCADE)
    done = models.IntegerField(default=0)

    def __str__(self):
        return '%s, %d' % (self.version, self.done)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    class Meta:
        verbose_name_plural = 'release progress'
