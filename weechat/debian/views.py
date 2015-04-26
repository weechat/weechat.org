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

"""Views for Debian repositories."""

from datetime import datetime
import gzip
from os import path, stat
import re

from django.shortcuts import render_to_response
from django.template import RequestContext

from weechat.common.path import repo_path_join
from weechat.debian.models import Repo


def repos(request, files=''):
    """Page with debian repositories."""
    repositories = []
    debpkgs = []
    try:
        repositories = (Repo.objects.all().filter(visible=1)
                        .order_by('priority'))
        for repo in repositories:
            repopkgs = []
            for arch in repo.arch.split(','):
                build = {
                    'id': '%s_%s' % (repo.name, repo.version.version),
                    'repo': repo,
                    'arch': arch,
                    'date': None,
                    'files': [],
                }
                filename = repo.path_packages_gz(arch)
                build['date'] = stat(filename).st_mtime
                _file = gzip.open(filename, 'rb')
                if _file:
                    pkg = {}
                    for line in _file.readlines():
                        line = line.strip()
                        if len(line) == 0:
                            if pkg:
                                pkg['repoarch'] = '%s_%s' % (
                                    repo.name, repo.version.version)
                                pkg['repo'] = repo
                                pkg['arch'] = arch
                                pkgfilename = repo_path_join(repo.domain,
                                                             pkg['Filename'])
                                fstat = stat(pkgfilename)
                                pkg['size'] = fstat.st_size
                                date_time = datetime.fromtimestamp(
                                    fstat.st_mtime)
                                pkg['builddate'] = date_time.strftime(
                                    '%Y-%m-%d')
                                pkg['buildtime'] = date_time.strftime('%H:%M')
                                pkg['builddatetime'] = pkg['builddate'] + \
                                    pkg['buildtime']
                                pkg['basename'] = \
                                    path.basename(pkg['Filename'])
                                pkg['anchor'] = '%s_%s_%s_%s' % (
                                    repo.name, repo.version.codename,
                                    pkg['Version'], arch)
                                if 'Source' not in pkg:
                                    pkg['Source'] = pkg['Package']
                                repopkgs.append(pkg)
                            pkg = {}
                        match = re.match('^([^ ]+): (.*)$', line)
                        if match:
                            pkg[match.group(1)] = match.group(2)
                    _file.close()
            debpkgs.extend(sorted(repopkgs, key=lambda p: p['builddatetime'],
                                  reverse=True))
    except:
        pass
    return render_to_response(
        'download/debian.html',
        {
            'debpkgs': debpkgs,
            'allfiles': files == 'files',
            'repositories': repositories,
        },
        context_instance=RequestContext(request))
