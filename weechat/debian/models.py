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

"""Models for Debian repositories."""

from django.db import models
from django.db.models.signals import post_save

from weechat.common.i18n import i18n_autogen
from weechat.common.path import repo_path_join


class Version(models.Model):
    """Version of a Debian repository (codename + version).

    Examples: (wheezy, stable), (jessie, testing), (sid, unstable), ...
    """
    codename = models.CharField(max_length=64, primary_key=True)
    version = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s (%s)' % (self.codename, self.version)


class Builder(models.Model):
    """The nick and name of person building packages in this repository."""
    nick = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.nick)


class Repo(models.Model):
    """A Debian repository."""
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    version = models.ForeignKey(Version)
    domain = models.CharField(max_length=128)
    arch = models.CharField(max_length=128)
    builder = models.ForeignKey(Builder)
    message = models.CharField(max_length=1024, blank=True)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s, %s (%s) (%d)' % (
            self.name,
            self.version,
            'active' if self.active else 'discontinued',
            self.arch,
            self.priority)

    def path_packages_gz(self, arch):
        """Return path/name to the Packages.gz file of repository."""
        return repo_path_join(self.domain, 'dists',
                              self.version.codename, 'main',
                              'binary-%s' % arch, 'Packages.gz')

    class Meta:
        ordering = ['priority']


def handler_repo_saved(sender, **kwargs):
    strings = []
    for repo in Repo.objects.order_by('priority'):
        if repo.message:
            strings.append(repo.message)
    i18n_autogen('debian', 'repo', strings)

post_save.connect(handler_repo_saved, sender=Repo)
