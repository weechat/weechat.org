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

"""Models for Debian repositories."""

from django.db import models
from django.db.models.signals import post_save

from weechat.common.i18n import i18n_autogen
from weechat.common.path import repo_path_join


class Version(models.Model):
    """Version of a Debian repository (codename + version).

    Examples: (wheezy, stable), (jessie, testing), (sid, unstable), etc.
    """
    codename = models.CharField(max_length=64, primary_key=True)
    version = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.codename} ({self.version})'


class Builder(models.Model):
    """The nick and name of person building packages in this repository."""
    nick = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name} ({self.nick})'


class Repo(models.Model):
    """A Debian repository."""
    visible = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    url = models.CharField(max_length=512)
    arch = models.CharField(max_length=128)
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE)
    # in hours, 0 = unknown frequency (next build date is not displayed)
    build_frequency = models.IntegerField(default=24)
    message = models.CharField(max_length=1024, blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        visible = 'visible' if self.visible else 'hidden'
        active = 'active' if self.active else 'discontinued'
        return (f'{self.name} {self.version}, {visible}, {active} '
                f'({self.arch}) ({self.priority})')

    def path_packages_gz(self, arch):
        """Return path/name to the Packages.gz file of repository."""
        return repo_path_join(self.name, 'dists',
                              self.version.codename, 'main',
                              f'binary-{arch}', 'Packages.gz')

    def apt_url(self):
        """
        Return the URL to use with apt for binary packages,
        for example: "deb https://weechat.org/debian sid main".
        """
        return f'deb {self.url} {self.version.codename} main'

    def apt_url_src(self):
        """
        Return the URL to use with apt for sources packages,
        for example: "deb-src https://weechat.org/debian sid main".
        """
        return f'deb-src {self.url} {self.version.codename} main'

    class Meta:
        """Sort Repos by priority."""
        ordering = ['priority']


def handler_repo_saved(sender, **kwargs):
    """Handler called when a Repo is saved."""
    # pylint: disable=unused-argument
    strings = []
    for repo in Repo.objects.order_by('priority'):
        if repo.message:
            strings.append(repo.message)
    i18n_autogen('debian', 'repo', strings)


post_save.connect(handler_repo_saved, sender=Repo)
