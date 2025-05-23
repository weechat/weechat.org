#
# SPDX-FileCopyrightText: 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

from datetime import date, datetime
from hashlib import sha1, sha512
import os
import sys

import pytz

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save

from weechat.common.models import Project
from weechat.common.path import files_path_join
from weechat.common.tracker import repo_link_file, repo_link_release
from weechat.common.utils import version_to_list

PACKAGES_COMPRESSION_EXT = (
    'gz',
    'xz',
)


class Release(models.Model):
    """A WeeChat release."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    date = models.DateField(blank=True, null=True)
    security_issues_fixed = models.IntegerField(default=0)
    securityfix = models.CharField(max_length=256, blank=True)

    def __str__(self):
        security_fix = (f', {self.security_issues_fixed} SECURITY FIX'
                        if self.security_issues_fixed > 0 else '')
        fixed_in = (f', fix in: {", ".join(self.securityfix.split(","))}'
                    if self.securityfix else '')
        return (
            f'{self.project.name} {self.version} '
            f'({self.date}){security_fix}{fixed_in}'
        )

    def next_stable_date(self):
        """Return the next stable release date (only for "devel" version)."""
        if self.version != 'devel':
            return None
        next_stable = self.description.split('-')[0]
        try:
            return Release.objects.get(
                project__name=self.project.name,
                version=next_stable,
            ).date
        except ObjectDoesNotExist:
            return None

    def security_fixed_versions(self):
        """Return the list of versions fixing security issues."""
        return self.securityfix.split(',')

    def changelog_url(self):
        """Return URL to ChangeLog file."""
        version = self.description if self.version == 'stable' else self.version
        if version == 'devel':
            # devel version: link to CHANGELOG.md
            return repo_link_file(self.project.name, 'main', 'CHANGELOG.md')
        if version_to_list(version) >= [4, 4]:
            # version ≥ 4.4.0: link to release on GitHub
            return repo_link_release(self.project.name, version)
        # version < 4.4.0: link to ChangeLog-x.y.z.html
        filename = f'ChangeLog-{version}.html'
        return f'/files/doc/{self.project.name}/{filename}'

    def upgrading_url(self):
        """Return URL to upgrade guidelines."""
        version = self.description if self.version == 'stable' else self.version
        if version == 'devel':
            # devel version: link to UPGRADING.md
            return repo_link_file(self.project.name, 'main', 'UPGRADING.md')
        if version_to_list(version) >= [4, 4]:
            # version ≥ 4.4.0: link to UPGRADING.md of this version
            return repo_link_file(self.project.name, f'v{version}', 'UPGRADING.md')
        # version < 4.4.0: link to ReleaseNotes-x.y.z.html
        filename = f'ReleaseNotes-{version}.html'
        return f'/files/doc/{self.project.name}/{filename}'

    @property
    def is_released(self):
        """Return True if the version is released."""
        stable_version = (Release.objects
                          .get(
                              project__name=self.project.name,
                              version='stable',
                          ).description)
        stable_version_list = version_to_list(stable_version)
        return version_to_list(self.version) <= stable_version_list

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
        return f'{self.type} - {self.description} ({self.priority})'

    def htmldir(self):
        """Return the HTML directory for the type of package."""
        if self.directory != '':
            return f'/{self.directory}'
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
        return f'{self.version.version}-{self.type.type}, {string}'

    def fullname(self):
        """Return the path for package."""
        if self.filename:
            return files_path_join(self.type.directory, self.filename)
        if self.directory:
            return files_path_join(self.directory)
        return ''

    def fullname_pgp_sig(self):
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

    def has_pgp_sig(self):
        """Checks if the package has a GPG signature."""
        return os.path.isfile(self.fullname_pgp_sig())

    def exists(self):
        """Checks if the package exists (on disk)."""
        return os.path.exists(self.fullname())

    def filesize(self):
        """Return the size of package, in bytes (as string)."""
        try:
            return str(os.path.getsize(self.fullname()))
        except:  # noqa: E722  pylint: disable=bare-except
            return ''

    def filedate(self):
        """Return the package date/time."""
        try:
            timezone = pytz.timezone(settings.TIME_ZONE)
            return datetime.fromtimestamp(os.path.getmtime(self.fullname()),
                                          tz=timezone)
        except:  # noqa: E722  pylint: disable=bare-except
            return ''

    class Meta:
        ordering = ['version', '-type__priority']


def handler_package_saved(sender, **kwargs):
    """Compute SHA-1 and SHA-512 of file."""
    # pylint: disable=unused-argument
    try:
        package = kwargs['instance']
        if package.filename and package.version.version != 'devel':
            with open(package.fullname(), 'rb') as _file:
                package.sha1sum = sha1(_file.read()).hexdigest()
            with open(package.fullname(), 'rb') as _file:
                package.sha512sum = sha512(_file.read()).hexdigest()
    except:  # noqa: E722  pylint: disable=bare-except
        pass


def make_symlink(link_name, target):
    """Create a symbolic link (overwrite link_name if existing)."""
    print(f'Making symlink: {link_name} -> {target}')
    tmp_name = f'{link_name}.__tmp__'
    os.symlink(target, tmp_name)
    os.rename(tmp_name, link_name)


def set_stable_version(project, version):
    """
    Set the stable version for a project and update all symbolic links to docs
    and packages.
    """
    # set stable version in database
    print(f'Setting stable release to {version} in project {project}')
    if Release.objects.filter(project__name=project, version='stable').exists():
        release = Release.objects.get(project__name=project, version='stable')
    else:
        release = Release(
            project=Project.objects.get(name=project),
            version='stable',
        )
    release.description = version
    release.date = date.today()
    release.security_issues_fixed = 0
    release.securityfix = ''
    release.save()

    # update package symbolic links
    for ext in PACKAGES_COMPRESSION_EXT:
        make_symlink(
            files_path_join('src', f'{project}-stable.tar.{ext}'),
            f'{project}-{version}.tar.{ext}',
        )
        make_symlink(
            files_path_join('src', f'{project}-stable.tar.{ext}.asc'),
            f'{project}-{version}.tar.{ext}.asc',
        )

    # update doc symbolic links
    doc_symlinks = (
        ('stable', version),
    )
    for link_name, filename in doc_symlinks:
        make_symlink(
            files_path_join('doc', project, link_name),
            filename,
        )


def set_devel_version(project, version):
    """Set the devel version for a project."""
    print(f'Setting devel release to {version} in project {project}')
    if Release.objects.filter(project__name=project, version='devel').exists():
        release = Release.objects.get(project__name=project, version='devel')
    else:
        release = Release(
            project=Project.objects.get(name=project),
            version='devel',
        )
    release.description = version
    release.save()


def add_release(project, version):
    """Add a project release with its packages."""
    print(f'Adding release {version} and packages in project {project}')
    if Release.objects.filter(project__name=project, version=version).exists():
        release = Release.objects.get(project__name=project, version=version)
    else:
        release = Release(
            project=Project.objects.get(name=project),
            version=version,
        )
    release.description = ''
    release.date = date.today()
    release.security_issues_fixed = 0
    release.securityfix = ''
    release.save()
    for ext in PACKAGES_COMPRESSION_EXT:
        Package.objects.filter(
            version__project__name=project,
            filename=f'{project}-{version}.tar.{ext}'
        ).delete()
        package = Package(
            version=release,
            type=Type.objects.get(type=f'src1-{ext}'),
            filename=f'{project}-{version}.tar.{ext}',
        )
        package.save()

    # if the version added is higher than current stable (or no current stable):
    #   1. update stable version
    #   2. set next devel version if version ends with ".0" (feature, not patch)
    version_list = version_to_list(version)
    try:
        stable_version = (
            Release.objects.get(project__name=project, version='stable').description
        )
    except ObjectDoesNotExist:
        stable_version = '0'
    stable_version_list = version_to_list(stable_version)
    if version_list > stable_version_list:
        # update stable version
        set_stable_version(project, version)
        # set next devel version
        if version_list[-1] == 0:
            next_devel = version_list[:]
            next_devel[-2] += 1
            next_devel[-1] = 0
            next_devel_string = '.'.join([str(v) for v in next_devel]) + '-dev'
            set_devel_version(project, next_devel_string)


def release_action(action, project, version):
    """Run a release action."""
    if action == 'stable':
        set_stable_version(project, version)
    elif action == 'devel':
        set_devel_version(project, version)
    elif action == 'add':
        add_release(project, version)
    else:
        print(f'ERROR: unsupported release action: "{action}"')
        sys.exit(1)


pre_save.connect(handler_package_saved, sender=Package)
