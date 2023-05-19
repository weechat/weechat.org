#
# Copyright (C) 2003-2023 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for "doc" menu."""

from datetime import datetime
from math import ceil
import os
import pytz

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext

from weechat.common.models import Project
from weechat.common.path import files_path_join
from weechat.common.utils import version_to_tuple
from weechat.doc.models import (
    Language,
    Version,
    Doc,
    Security,
)
from weechat.download.models import Release

I18N_MAINTAINER = {
    'cs': ('-', ''),
    'de': ('nils_2', 'Nils Görs'),
    'en': ('FlashCode', 'Sébastien Helleu'),
    'es': ('-', ''),
    'fr': ('FlashCode', 'Sébastien Helleu'),
    'hu': ('-', ''),
    'it': ('-', ''),
    'ja': ('R. Ayanokouzi', 'Ryuunosuke Ayanokouzi'),
    'pl': ('soltys', 'Krzysztof Korościk'),
    'pt': ('', 'Vasco Almeida'),
    'pt_BR': ('-', ''),
    'ru': ('-', ''),
    'sr': ('', 'Ivan Pešić'),
    'tr': ('-', ''),
}

DOC_SHORTCUT_ALIAS = {
    'faq': 'faq',
    'quick': 'quickstart',
    'plugin': 'plugin_api',
    'api': 'plugin_api',
    'relay': 'relay_protocol',
}


def get_i18n_stats(project):
    """Return i18n stats, as a dictionary.

    The returned dictionary has following keys:
    - date: date/time of last translations update
    - langs: a dictionary with info about status of this language.
    """
    # pylint: disable=too-many-locals
    try:
        timezone = pytz.timezone(settings.TIME_ZONE)
        filename = files_path_join('stats', f'i18n_{project}.txt')
        date = datetime.fromtimestamp(os.path.getmtime(filename), tz=timezone)
        with open(filename, 'r', encoding='utf-8') as _file:
            langs = []
            for line in _file:
                items = line.split(':')
                if len(items) == 2:
                    lang = items[0]
                    count = items[1].split(',')
                    translated = float(count[0])
                    fuzzy = float(count[1])
                    untranslated = float(count[2])
                    total = translated + fuzzy + untranslated
                    if total != 0:
                        pct_fuzzy = int(ceil((fuzzy * 100) / total))
                        pct_untrans = int(
                            ceil((untranslated * 100) / total))
                        pct_trans = max(100 - pct_fuzzy - pct_untrans, 0)
                        nick, name = I18N_MAINTAINER.get(lang, ('-', ''))
                        langs.append({
                            'lang': lang,
                            'lang_i18n': (gettext(Language.LANG_I18N[lang])
                                          if lang in Language.LANG_I18N
                                          else lang),
                            'nick': nick,
                            'name': name,
                            'translated': int(translated),
                            'pct_translated': pct_trans,
                            'fuzzy': int(fuzzy),
                            'pct_fuzzy': pct_fuzzy,
                            'untranslated': int(untranslated),
                            'pct_untranslated': pct_untrans,
                            'total': int(total),
                        })
        return {'date': date, 'langs': langs}
    except:  # noqa: E722  pylint: disable=bare-except
        return None


def get_bestlang(request, languages):
    """
    Return the first language in HTTP_ACCEPT_LANGUAGE which has at least
    one doc in WeeChat.
    """
    for item in request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(','):
        for item2 in item.split(';'):
            lang = item2[:2]
            if lang != 'q=':
                for onelang in languages:
                    if onelang.lang == lang:
                        return lang
    return ''


def documentation(request, project='weechat', version='stable'):
    """Page with docs for stable or devel version."""
    # pylint: disable=too-many-locals,too-many-branches,too-many-nested-blocks
    get_object_or_404(Project, name=project, visible=1)
    timezone = pytz.timezone(settings.TIME_ZONE)
    languages = (Language.objects
                 .filter(
                     project__name=project,
                     project__visible=1,
                 )
                 .order_by('priority'))
    bestlang = get_bestlang(request, languages)
    versions = Version.objects.all().order_by('priority')
    docs = (Doc.objects
            .filter(
                project__name=project,
                project__visible=1,
            )
            .order_by('version__priority', 'priority'))
    doc_list = []
    doc_list2 = []
    build_date = None
    for doc in docs:
        if doc.version.version != '-':
            docv = (Release.objects
                    .get(
                        project__name=project,
                        project__visible=1,
                        version=doc.version.version,
                    )
                    .description)
        else:
            docv = doc.version.version
        stable_devel = 'devel' if docv.find('-') > 0 else 'stable'
        if stable_devel == version or docv == '-':
            files = []
            for lang in languages:
                if doc.url:
                    files.append((lang, '', doc.url if lang.lang == 'en' else ''))
                else:
                    name = (f'{project}/{doc.version.directory}/'
                            f'weechat_{doc.name}.{lang.lang}.html')
                    full_name = files_path_join('doc', name)
                    if os.path.exists(full_name):
                        if not build_date:
                            build_date = datetime.fromtimestamp(
                                os.path.getmtime(full_name),
                                tz=timezone)
                        files.append((lang, os.path.normpath(name), ''))
                    else:
                        files.append((lang, '', ''))
            if docv == '-':
                doc_list.append((doc, files))
            else:
                doc_list2.append((doc, files))
    try:
        doc_version = (Release.objects
                       .get(
                           project__name=project,
                           project__visible=1,
                           version=version,
                       )
                       .description)
    except ObjectDoesNotExist:
        doc_version = None
    return render(
        request,
        'doc/doc_version.html',
        {
            'project': project,
            'version': version,
            'languages': languages,
            'bestlang': bestlang,
            'versions': versions,
            'doc_list': doc_list + doc_list2,
            'build_date': build_date,
            'i18n': get_i18n_stats(project),
            'doc_version': doc_version,
        },
    )


def documentation_link(request, project='weechat', version='stable', name=None,
                       lang='en'):
    """
    Shortcuts to docs, with English and stable version as default.

    For example:
      /doc/api          => /files/doc/stable/weechat_plugin_api.en.html
      /doc/api/fr       => /files/doc/stable/weechat_plugin_api.fr.html
      /doc/devel/api/fr => /files/doc/devel/weechat_plugin_api.fr.html
      /doc/user         => /files/doc/stable/weechat_user.en.html
    """
    if project and version and name and lang:
        get_object_or_404(Project, name=project, visible=1)
        doc_name = DOC_SHORTCUT_ALIAS.get(name, name)
        filename = f'weechat_{doc_name}.{lang}.html'
        full_name = files_path_join('doc', project, version, filename)
        if os.path.exists(full_name):
            return redirect(f'/files/doc/{project}/{version}/{filename}')
    return redirect('doc')


def security_all(request, project='weechat'):
    """Page with security vulnerabilities."""
    get_object_or_404(Project, name=project, visible=1)
    security_list = (Security.objects.all()
                     .filter(
                         project__name=project,
                         project__visible=1,
                         visible=1,
                     )
                     .order_by('-date'))
    return render(
        request,
        'doc/security.html',
        {
            'project': project,
            'security': True,
            'version': 'all',
            'security_list': security_list,
        },
    )


def security_wsa(request, project='weechat', wsa=''):
    """Page with security a single vulnerability."""
    get_object_or_404(Project, name=project, visible=1)
    context = {
        'project': project,
        'security': True,
        'version': 'wsa',
    }
    try:
        context['security_list'] = [
            Security.objects.get(
                project__name=project,
                project__visible=1,
                wsa=wsa,
            )
        ]
    except ObjectDoesNotExist:
        context['wsa_error'] = True
    return render(request, 'doc/security.html', context)


def is_security_affecting_release(security, release):
    """Return True if the Security issue is affecting the Release."""
    version_tuple = version_to_tuple(release.version)
    for version in security.affected.split(','):
        if '-' in version:
            version1, version2 = version.split('-', 1)
            version1 = version_to_tuple(version1)
            version2 = version_to_tuple(version2)
            if version1 <= version_tuple <= version2:
                return True
        else:
            if version_tuple == version_to_tuple(version):
                return True
    return False


def security_version(request, project='weechat', version=''):
    """Page with security vulnerabilities, by version or for a version."""
    get_object_or_404(Project, name=project, visible=1)
    security_list = (Security.objects.all()
                     .filter(
                         project__name=project,
                         project__visible=1,
                         visible=1,
                     )
                     .order_by('-date'))
    context = {
        'project': project,
        'security': True,
        'version': version,
    }
    if version:
        try:
            release = Release.objects.get(
                project__name=project,
                project__visible=1,
                version=version,
            )
            if not release.is_released:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            release = None
            context['version_error'] = True
        if release:
            context['security_list'] = [
                security for security in security_list
                if is_security_affecting_release(security, release)
            ]
    else:
        security_list_by_release = {}
        release_list = (Release.objects
                        .filter(
                            project__name=project,
                            project__visible=1,
                        )
                        .exclude(version='devel')
                        .exclude(version='stable')
                        .order_by('-date'))
        for release in release_list:
            if not release.is_released:
                continue
            security_list_by_release[release] = [
                security for security in security_list
                if is_security_affecting_release(security, release)
            ]
        context['security_list_by_release'] = security_list_by_release
    return render(request, 'doc/security.html', context)
