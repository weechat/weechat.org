#
# Copyright (C) 2003-2021 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for "download" menu."""

import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from weechat.download.models import Release, Package
from weechat.download.models import ReleaseTodo, ReleaseProgress


def get_release_progress():
    """
    Return release progress info as a tuple (version, date, todo, done, pct).
    """
    rel_todo = ReleaseTodo.objects.all().order_by('priority')
    next_rel = Release.objects.get(version='devel')
    next_rel_version = re.sub('-.*', '', next_rel.description)
    next_rel_date = next_rel.date
    rel_progress = ReleaseProgress.objects.all()
    done = -1
    pct = 0
    if len(rel_todo) > 0 and len(rel_progress) > 0 \
            and rel_progress[0].done >= 0:
        done = rel_progress[0].done
        pct = int((float(done) / len(rel_todo)) * 100)
        if pct < 0:
            pct = 0
        if pct > 100:
            pct = 100
        next_rel_version = rel_progress[0].version.version
        next_rel_date = rel_progress[0].version.date
    return {
        'version': next_rel_version,
        'date': next_rel_date,
        'todo': rel_todo,
        'done': done,
        'pct': pct,
    }


def packages(request, version='stable'):
    """Page with packages for a version (stable, devel, all, old, or x.y.z)."""
    package_list = None
    release_progress = None
    try:
        if version == 'stable':
            stable_desc = Release.objects.get(version='stable').description
            package_list = (Package.objects.all().filter(version=stable_desc)
                            .order_by('type__priority'))
        elif version == 'devel':
            package_list = (Package.objects.all().filter(version='devel')
                            .order_by('type__priority'))
        elif version == 'all':
            package_list = (Package.objects.all().exclude(version='devel')
                            .order_by('-version__date', 'type__priority'))
        elif version == 'old':
            stable_desc = Release.objects.get(version='stable').description
            package_list = (Package.objects.all().exclude(version='devel')
                            .exclude(version=stable_desc)
                            .order_by('-version__date', 'type__priority'))
        else:
            package_list = (Package.objects.filter(version=version)
                            .order_by('type__priority'))
        release_progress = get_release_progress()
    except ObjectDoesNotExist:
        package_list = None
        release_progress = None
    return render(
        request,
        'download/packages.html',
        {
            'version': version,
            'package_list': package_list,
            'release_progress': release_progress,
        },
    )


def package_checksums(request, version, checksum_type):
    """Page with checksums of packages in a version."""
    package_list = (Package.objects.filter(version=version)
                    .order_by('type__priority'))
    checksums = []
    for package in package_list:
        checksum = package.checksum()
        if checksum:
            checksums.append(f'{checksum}  {package.filename}')
    response = HttpResponse('\n'.join(checksums), content_type='text/plain')
    response['Content-disposition'] = (f'inline; filename=weechat-'
                                       f'{version}-{checksum_type}.txt')
    return response


def release(request):
    """Page with release in progress."""
    return render(
        request,
        'download/release.html',
        {
            'release_progress': get_release_progress(),
        },
    )
