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

from os import path
import re

from django.shortcuts import render_to_response
from django.template import RequestContext

from weechat.common.path import files_path_join
from weechat.download.models import Release, Package, Security
from weechat.download.models import ReleaseTodo, ReleaseProgress


def get_release_progress():
    """
    Return release progress info as a tuple (version, date, todo, done, pct).
    """
    rel_todo = ReleaseTodo.objects.all().order_by('priority')
    next_rel = Release.objects.get(version='devel')
    next_rel_version = re.sub('-.*', '', next_rel.description)
    rel_progress = ReleaseProgress.objects.filter(version=next_rel_version)
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
    return \
        {
            'version': next_rel_version,
            'date': next_rel.date,
            'todo': rel_todo,
            'done': done,
            'pct': pct
        }


def packages(request, version='stable'):
    """Page with packages for a version (stable, devel, all, old, or x.y.z)."""
    package_list = None
    if version == 'stable':
        stable_desc = Release.objects.get(version='stable').description
        package_list = Package.objects.all().filter(version=stable_desc) \
            .order_by('type__priority')
    elif version == 'devel':
        package_list = Package.objects.all().filter(version='devel') \
            .order_by('type__priority')
    elif version == 'all':
        package_list = Package.objects.all().exclude(version='devel') \
            .order_by('-version__date', 'type__priority')
    elif version == 'old':
        stable_desc = Release.objects.get(version='stable').description
        package_list = Package.objects.all().exclude(version='devel') \
            .exclude(version=stable_desc) \
            .order_by('-version__date', 'type__priority')
    else:
        package_list = Package.objects.filter(version=version) \
            .order_by('type__priority')
    return render_to_response(
        'download/packages.html',
        {
            'version': version,
            'package_list': package_list,
            'release_progress': get_release_progress(),
        },
        context_instance=RequestContext(request))


def release(request):
    """Page with release in progress."""
    return render_to_response(
        'download/release.html',
        {
            'release_progress': get_release_progress(),
        },
        context_instance=RequestContext(request))


def security(request):
    """Page with security vulnerabilities."""
    security_list = Security.objects.all().filter(visible=1).order_by('-date')
    return render_to_response('download/security.html',
                              {'security_list': security_list},
                              context_instance=RequestContext(request))
