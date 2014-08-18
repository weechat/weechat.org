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

"""Views for "dev" menu."""

import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext_lazy

from weechat.common.path import files_path_join
from weechat.common.templatetags.version import version_as_int
from weechat.dev.models import Task
from weechat.download.models import Release

INFO_KEYS = (
    (
        'stable',
        gettext_lazy('stable version'),
    ),
    (
        'stable_number',
        gettext_lazy('stable version, as number, like plugin API: '
                     'info_get("version_number")'),
    ),
    (
        'stable_date',
        '%s %s' % (gettext_lazy('date of stable version'), '(YYYY-MM-DD)'),
    ),
    (
        'devel',
        gettext_lazy('development version'),
    ),
    (
        'git',
        gettext_lazy('output of "git rev-parse HEAD" for sources repository'),
    ),
    (
        'git_scripts',
        gettext_lazy('output of "git rev-parse HEAD" for scripts repository'),
    ),
    (
        'next_stable',
        gettext_lazy('next stable version'),
    ),
    (
        'next_stable_number',
        gettext_lazy('next stable version, as number, like plugin API: '
                     'info_get("version_number")'),
    ),
    (
        'next_stable_date',
        '%s (YYYY-MM-DD)' % gettext_lazy('approximate date of next '
                                         'stable version'),
    ),
    (
        'all',
        gettext_lazy('all infos (one info by line, format: "info:value")'),
    ),
)


def roadmap(request, allversions=False):
    """Page with roadmap for future or all versions."""
    if allversions:
        task_list = Task.objects.all().filter(visible=1).order_by('version',
                                                                  'priority')
    else:
        task_list = Task.objects.all().filter(visible=1).filter(
            version__gt=Release.objects.get(
                version='stable').description).order_by('version', 'priority')
    return render_to_response(
        'dev/roadmap.html',
        {
            'task_list': task_list,
            'allversions': allversions,
        },
        context_instance=RequestContext(request))


def stats_repo(request, stats='weechat'):
    """Page with statistics about source code (git repositories)."""
    repository = ''
    sloc = ''
    sloc_lang = ''
    svg_list = ['authors', 'files_type', 'commits_year', 'commits_year_month',
                'commits_day', 'commits_day_max', 'commits_day_week',
                'commits_hour_day', 'commits_hour_week']
    git_commits = ['?', '?', '?', '?']
    scripts_downloads = None

    try:
        with open(files_path_join('stats',
                                  'git_%s_commits.txt' % stats), 'r') as _file:
            git_commits = _file.read().split(',')
    except:
        pass

    if stats in ('weechat', 'qweechat'):
        try:
            with open(files_path_join('stats',
                                      'sloc_%s.txt' % stats), 'r') as _file:
                sloc = _file.read()
        except:
            pass

    if stats == 'weechat':
        repository = ('https://github.com/weechat/weechat')
        sloc_lang = 'C'
        svg_list += ['commits_version', 'commits_other_clients']
    elif stats == 'scripts':
        repository = ('https://github.com/weechat/scripts')
        svg_list += ['downloads']
        try:
            with open(files_path_join('stats',
                                      'scripts_downloads.txt'), 'r') as _file:
                scripts_downloads = _file.read()
        except:
            pass
    elif stats == 'qweechat':
        repository = ('https://github.com/weechat/qweechat')
        sloc_lang = 'Python'
    elif stats == 'weechat.org':
        repository = ('https://github.com/weechat/weechat.org')
    return render_to_response(
        'dev/stats.html',
        {
            'stats': stats,
            'repository': repository,
            'sloc': sloc,
            'sloc_lang': sloc_lang,
            'git_commits_last_week': git_commits[0],
            'git_commits_last_month': git_commits[1],
            'git_commits_last_year': git_commits[2],
            'git_commits_total': git_commits[3],
            'scripts_downloads': scripts_downloads,
            'svg_list': svg_list,
        },
        context_instance=RequestContext(request))


def get_info(name, version):
    """Get an info."""
    if name == 'stable':
        return version['stable'].description
    elif name == 'stable_number':
        return version_as_int(version['stable'].description)
    elif name == 'stable_date':
        return str(version['stable'].date)
    elif name == 'devel':
        return version['devel'].description
    elif name == 'git':
        git = ''
        try:
            with open(files_path_join('git_sources_head.txt'), 'r') as _file:
                git = _file.read().strip()
        except:
            pass
        return git
    elif name == 'git_scripts':
        git = ''
        try:
            with open(files_path_join('git_scripts_head.txt'), 'r') as _file:
                git = _file.read().strip()
        except:
            pass
        return git
    elif name == 'next_stable':
        return re.sub('-.*', '', version['devel'].description)
    elif name == 'next_stable_number':
        return version_as_int(version['devel'].description)
    elif name == 'next_stable_date':
        return str(version['devel'].date)
    elif name == 'all':
        infos = []
        for key in INFO_KEYS:
            if key[0] != name:
                infos.append('%s:%s' % (key[0], get_info(key[0], version)))
        return '\n'.join(infos)
    return ''


def info(request, name=None):
    """Page with one or all available infos."""
    version = {
        'stable': Release.objects.get(version='stable'),
        'devel': Release.objects.get(version='devel'),
    }
    if name:
        return render_to_response('dev/info.html',
                                  {'info': get_info(name, version)},
                                  context_instance=RequestContext(request))
    else:
        infos = []
        for oneinfo in INFO_KEYS:
            value = get_info(oneinfo[0], version)
            if oneinfo[0].endswith('_number'):
                value = '%s (0x%08lx)' % (value, value)
            infos.append((oneinfo[0], value, oneinfo[1]))
        return render_to_response('dev/info_list.html',
                                  {'infos': infos},
                                  context_instance=RequestContext(request))
