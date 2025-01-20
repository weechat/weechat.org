#
# Copyright (C) 2003-2024 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for "dev" menu."""

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext, gettext_lazy

from weechat.common.path import files_path_join, media_path_join
from weechat.common.templatetags.version import version_as_int
from weechat.common.utils import version_to_list
from weechat.dev.models import Task
from weechat.download.models import Release

INFO_KEYS = (
    (
        'stable',
        gettext_lazy('Stable version.'),
    ),
    (
        'stable_number',
        gettext_lazy('Stable version, as number, like plugin API: '
                     'info_get("version_number").'),
    ),
    (
        'stable_date',
        gettext_lazy('Date of stable version (format: "YYYY-MM-DD").'),
    ),
    (
        'devel',
        gettext_lazy('Development version.'),
    ),
    (
        'git',
        gettext_lazy('Output of "git rev-parse HEAD" for sources '
                     'repository.'),
    ),
    (
        'git_scripts',
        gettext_lazy('Output of "git rev-parse HEAD" for scripts '
                     'repository.'),
    ),
    (
        'next_stable',
        gettext_lazy('Next stable version.'),
    ),
    (
        'next_stable_number',
        gettext_lazy('Next stable version, as number, like plugin API: '
                     'info_get("version_number").'),
    ),
    (
        'next_stable_date',
        gettext_lazy('Approximate date of next stable version '
                     '(format: "YYYY-MM-DD").'),
    ),
    (
        'release_signing_fingerprint',
        gettext_lazy('Release signing key fingerprint '
                     '(format: PGP fingerprint).'),
    ),
    (
        'release_signing_key',
        gettext_lazy('Release signing key '
                     '(format: PGP public key as binary file).'),
    ),
    (
        'release_signing_key_asc',
        gettext_lazy('Release signing key '
                     '(format: PGP public key as ASCII file).'),
    ),
    (
        'debian_repository_signing_fingerprint',
        gettext_lazy('Debian/Ubuntu repository signing key fingerprint '
                     '(format: PGP fingerprint).'),
    ),
    (
        'debian_repository_signing_key',
        gettext_lazy('Debian/Ubuntu repository signing key '
                     '(format: PGP public key as binary file).'),
    ),
    (
        'debian_repository_signing_key_asc',
        gettext_lazy('Debian/Ubuntu repository signing key '
                     '(format: PGP public key as ASCII file).'),
    ),
    (
        'all',
        gettext_lazy('All non-binary infos '
                     '(one info by line, format: "info:value").'),
    ),
)

INFO_PGP_KEYS_BIN = (
    'release_signing_key',
    'debian_repository_signing_key',
)
INFO_PGP_KEYS_ASC = (
    'release_signing_key_asc',
    'debian_repository_signing_key_asc',
)
INFO_PGP_KEYS = INFO_PGP_KEYS_BIN + INFO_PGP_KEYS_ASC

PGP_KEYS = {
    'release_signing': 'A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8',
    'debian_repository_signing': '11E9DE8848F2B65222AA75B8D1820DB22A11534E'
}


def roadmap(request, versions='future'):
    """Page with roadmap for future or all versions."""
    task_list = None
    try:
        v_stable = version_to_list(
            Release.objects.get(project__name='weechat',
                                version='stable').description
        )
        all_tasks = Task.objects.all().filter(visible=1).order_by('priority')
        reverse = False
        if versions == 'future':
            # future versions
            tasks = [task for task in all_tasks
                     if version_to_list(task.version.version) > v_stable]
        else:
            # already released versions
            tasks = [task for task in all_tasks
                     if version_to_list(task.version.version) <= v_stable]
            reverse = True
        task_list = sorted(
            tasks,
            key=lambda task: version_to_list(task.version.version),
            reverse=reverse,
        )
    except ObjectDoesNotExist:
        task_list = None
    return render(
        request,
        'dev/roadmap.html',
        {
            'task_list': task_list,
            'versions': versions,
        },
    )


def stats_repo(request, stats='weechat'):
    """Page with statistics about source code (git repositories)."""
    repository = ''
    sloc = ''
    sloc_lang = ''
    svg_list = ['authors', 'tickets_author', 'files_type', 'commits_year',
                'commits_year_month', 'commits_day', 'commits_day_max',
                'commits_day_week', 'commits_hour_day', 'commits_hour_week']
    git_commits = ['?', '?', '?', '?']
    scripts_downloads = None

    try:
        with open(files_path_join('stats', f'git_{stats}_commits.txt'),
                  'r', encoding='utf-8') as _file:
            git_commits = _file.read().strip().split(',')
    except:  # noqa: E722  pylint: disable=bare-except
        pass

    try:
        with open(files_path_join('stats', f'sloc_{stats}.txt'),
                  'r', encoding='utf-8') as _file:
            sloc = _file.read()
    except:  # noqa: E722  pylint: disable=bare-except
        pass

    if stats == 'weechat':
        repository = 'https://github.com/weechat/weechat'
        sloc_lang = 'C'
        svg_list += ['commits_version', 'commits_other_clients']
    elif stats == 'weechat-relay':
        repository = 'https://github.com/weechat/weechat-relay'
        sloc_lang = 'C'
    elif stats == 'scripts':
        repository = 'https://github.com/weechat/scripts'
        svg_list += ['downloads']
        try:
            with open(files_path_join('stats', 'scripts_downloads.txt'),
                      'r', encoding='utf-8') as _file:
                scripts_downloads = _file.read()
        except:  # noqa: E722  pylint: disable=bare-except
            pass
    elif stats == 'qweechat':
        repository = 'https://github.com/weechat/qweechat'
        sloc_lang = 'Python'
    elif stats == 'weechat.org':
        repository = 'https://github.com/weechat/weechat.org'
        sloc_lang = 'Python'
    return render(
        request,
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
    )


def get_info(name, version):
    """Get an info."""
    # pylint: disable=too-many-branches,too-many-return-statements
    next_stable = version['devel'].description.split('-')[0]
    if name == 'stable':
        return version['stable'].description
    if name == 'stable_number':
        return version_as_int(version['stable'].description)
    if name == 'stable_date':
        return str(version['stable'].date)
    if name == 'devel':
        return version['devel'].description
    if name == 'git':
        git = ''
        try:
            with open(files_path_join('git_sources_head.txt'),
                      'r', encoding='utf-8') as _file:
                git = _file.read().strip()
        except:  # noqa: E722  pylint: disable=bare-except
            pass
        return git
    if name == 'git_scripts':
        git = ''
        try:
            with open(files_path_join('git_scripts_head.txt'),
                      'r', encoding='utf-8') as _file:
                git = _file.read().strip()
        except:  # noqa: E722  pylint: disable=bare-except
            pass
        return git
    if name == 'next_stable':
        return next_stable
    if name == 'next_stable_number':
        return version_as_int(version['devel'].description)
    if name == 'next_stable_date':
        return str(version[next_stable].date)
    if name == 'release_signing_fingerprint':
        return PGP_KEYS['release_signing']
    if name == 'debian_repository_signing_fingerprint':
        return PGP_KEYS['debian_repository_signing']
    if name == 'release_signing_key':
        filename = PGP_KEYS['release_signing']
        with open(media_path_join('pgp', filename), 'rb') as _file:
            return _file.read()
    if name == 'release_signing_key_asc':
        filename = PGP_KEYS['release_signing'] + '.asc'
        with open(media_path_join('pgp', filename), 'r', encoding='utf-8') as _file:
            return _file.read()
    if name == 'debian_repository_signing_key':
        filename = PGP_KEYS['debian_repository_signing']
        with open(media_path_join('pgp', filename), 'rb') as _file:
            return _file.read()
    if name == 'debian_repository_signing_key_asc':
        filename = PGP_KEYS['debian_repository_signing'] + '.asc'
        with open(media_path_join('pgp', filename), 'r', encoding='utf-8') as _file:
            return _file.read()
    if name == 'all':
        infos = []
        for key in INFO_KEYS:
            if key[0] != name and key[0] not in INFO_PGP_KEYS:
                infos.append(f'{key[0]}:{get_info(key[0], version)}')
        return '\n'.join(infos)
    return ''


def info(request, name=None):
    """Page with one or all available infos."""
    try:
        version = {
            'stable': Release.objects.get(project__name='weechat', version='stable'),
            'devel': Release.objects.get(project__name='weechat', version='devel'),
        }
        next_stable = version['devel'].description.split('-')[0]
        version[next_stable] = Release.objects.get(project__name='weechat',
                                                   version=next_stable)
    except ObjectDoesNotExist:
        return render(
            request,
            'dev/info_list.html',
            {
                'infos': [],
            },
        )
    if name:
        if name in INFO_PGP_KEYS_BIN:
            response = HttpResponse(get_info(name, version),
                                    content_type='application/octet-stream')
            filename = f'weechat_{name}.pgp'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        if name in INFO_PGP_KEYS_ASC:
            response = HttpResponse(get_info(name, version),
                                    content_type='text/plain')
            filename = f'weechat_{name.removesuffix("_asc")}.asc'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        return render(
            request,
            'dev/info.html',
            {
                'info': get_info(name, version),
            },
            content_type='text/plain; charset=utf-8',
        )
    infos = []
    for oneinfo in INFO_KEYS:
        if oneinfo[0] in INFO_PGP_KEYS:
            value = gettext('(file)')
        else:
            value = get_info(oneinfo[0], version)
        if oneinfo[0].endswith('_number'):
            value = f'{value} ({value:#010x})'
        infos.append((oneinfo[0], value, oneinfo[1]))
    return render(
        request,
        'dev/info_list.html',
        {
            'infos': infos,
        },
    )
