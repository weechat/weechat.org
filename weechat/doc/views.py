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
# along with WeeChat.org.  If not, see <http://www.gnu.org/licenses/>.
#

"""Views for "doc" menu."""

from datetime import datetime
from math import ceil
import os
import pytz

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.translation import ugettext

from weechat.common.path import files_path_join
from weechat.doc.models import Language, Version, Doc, Security
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
    'tr': ('-', ''),
}

DOC_SHORTCUT_ALIAS = {
    'quick': 'quickstart',
    'plugin': 'plugin_api',
    'api': 'plugin_api',
    'relay': 'relay_protocol',
}


def get_i18n_stats():
    """Return i18n stats, as a dictionary.

    The returned dictionary has following keys:
    - date: date/time of last translations update
    - langs: a dictionary with info about status of this language.
    """
    try:
        timezone = pytz.timezone(settings.TIME_ZONE)
        filename = files_path_join('stats', 'i18n.txt')
        date = datetime.fromtimestamp(os.path.getmtime(filename), tz=timezone)
        with open(filename, 'r') as _file:
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
                        pct_untranslated = int(
                            ceil((untranslated * 100) / total))
                        pct_translated = 100 - pct_fuzzy - pct_untranslated
                        if pct_translated < 0:
                            pct_translated = 0
                        nick, name = I18N_MAINTAINER.get(lang, ('-', ''))
                        langs.append({
                            'lang': lang,
                            'lang_i18n': (ugettext(Language.LANG_I18N[lang])
                                          if lang in Language.LANG_I18N
                                          else lang),
                            'nick': nick,
                            'name': name,
                            'translated': int(translated),
                            'pct_translated': pct_translated,
                            'fuzzy': int(fuzzy),
                            'pct_fuzzy': pct_fuzzy,
                            'untranslated': int(untranslated),
                            'pct_untranslated': pct_untranslated,
                            'total': int(total),
                        })
        return {'date': date, 'langs': langs}
    except:  # noqa: E722
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


def documentation(request, version='stable'):
    """Page with docs for stable or devel version."""
    timezone = pytz.timezone(settings.TIME_ZONE)
    if version == 'old':
        doc_list = None
        try:
            doc_list = sorted(os.listdir(files_path_join('doc', 'old')),
                              reverse=True)
        except:  # noqa: E722
            pass
        return render(
            request,
            'doc/doc_version.html',
            {
                'version': version,
                'doc_list': doc_list,
            },
        )
    languages = Language.objects.all().order_by('priority')
    bestlang = get_bestlang(request, languages)
    versions = Version.objects.all().order_by('priority')
    docs = Doc.objects.all().order_by('version__priority', 'priority')
    doc_list = []
    doc_list2 = []
    for doc in docs:
        if doc.version.version != '-':
            docv = Release.objects.get(
                version=doc.version.version).description
        else:
            docv = doc.version.version
        stable_devel = 'devel' if docv.find('-') > 0 else 'stable'
        if stable_devel == version or docv == '-':
            files = []
            for lang in languages:
                name = '%s/weechat_%s.%s.html' % (
                    doc.version.directory, doc.name, lang.lang)
                full_name = files_path_join('doc', name)
                if os.path.exists(full_name):
                    files.append(
                        (
                            os.path.normpath(name),
                            datetime.fromtimestamp(os.path.getmtime(full_name),
                                                   tz=timezone),
                            lang,
                        )
                    )
                else:
                    files.append(['', '', lang.lang])
            if docv == '-':
                doc_list.append([doc, files])
            else:
                doc_list2.append([doc, files])
    try:
        doc_version = Release.objects.get(version=version).description
    except ObjectDoesNotExist:
        doc_version = None
    return render(
        request,
        'doc/doc_version.html',
        {
            'version': version,
            'languages': languages,
            'bestlang': bestlang,
            'versions': versions,
            'doc_list': doc_list + doc_list2,
            'i18n': get_i18n_stats(),
            'doc_version': doc_version,
        },
    )


def documentation_link(request, version='stable', name=None, lang='en'):
    """
    Shortcuts to docs, with English and stable version as default.

    For example:
      /doc/api          => /files/doc/stable/weechat_plugin_api.en.html
      /doc/api/fr       => /files/doc/stable/weechat_plugin_api.fr.html
      /doc/devel/api/fr => /files/doc/devel/weechat_plugin_api.fr.html
      /doc/user         => /files/doc/stable/weechat_user.en.html
    """
    if version and name and lang:
        doc_name = DOC_SHORTCUT_ALIAS.get(name, name)
        filename = 'weechat_%s.%s.html' % (doc_name, lang)
        full_name = files_path_join('doc', version, filename)
        if os.path.exists(full_name):
            return redirect('/files/doc/%s/%s' % (version, filename))
    return redirect('doc')


def security(request):
    """Page with security vulnerabilities."""
    security_list = Security.objects.all().filter(visible=1).order_by('-date')
    return render(
        request,
        'doc/security.html',
        {
            'security_list': security_list,
        },
    )
