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

"""Views for "doc" menu."""

from datetime import datetime
from math import ceil
from os import path, listdir

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext

from weechat.common.path import files_path_join
from weechat.doc.models import Language, Version, Doc
from weechat.download.models import Release

I18N_MAINTAINER = {
    'en': ('FlashCode', 'Sébastien Helleu'),
    'fr': ('FlashCode', 'Sébastien Helleu'),
    'it': ('Quizzlo', 'Marco Paolone'),
    'de': ('nils_2', 'Nils Görs'),
    'ja': ('R. Ayanokouzi', 'Ryuunosuke Ayanokouzi'),
    'pl': ('soltys', 'Krzysztof Korościk'),
    'ru': ('ixti', 'Aleksey Zapparov'),
    'pt_BR': ('ISF_ec09', 'Ivan Sichmann Freitas'),
    'tr': ('turgay', 'Hasan Kiran'),
    'es': ('-', ''),
    'cs': ('-', ''),
    'hu': ('-', ''),
}


def get_i18n_stats():
    """Return i18n stats, as a dictionary.

    The returned dictionary has following keys:
    - date: date/time of last translations update
    - langs: a dictionary with info about status of this language.
    """
    try:
        filename = files_path_join('stats', 'i18n.txt')
        date = datetime.fromtimestamp(path.getmtime(filename))
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
                        pct_untranslated = \
                            int(ceil((untranslated * 100) / total))
                        pct_translated = 100 - pct_fuzzy - pct_untranslated
                        if pct_translated < 0:
                            pct_translated = 0
                        langs.append({
                            'lang': lang,
                            'lang_i18n': ugettext(
                                Language.LANG_I18N[lang]),
                            'nick': I18N_MAINTAINER[lang][0],
                            'name': I18N_MAINTAINER[lang][1],
                            'translated': int(translated),
                            'pct_translated': pct_translated,
                            'fuzzy': int(fuzzy),
                            'pct_fuzzy': pct_fuzzy,
                            'untranslated': int(untranslated),
                            'pct_untranslated': pct_untranslated,
                            'total': int(total),
                        })
        return {'date': date, 'langs': langs}
    except:
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
    if version == 'old':
        doc_list = None
        try:
            doc_list = sorted(listdir(files_path_join('doc', 'old')),
                              reverse=True)
        except:
            pass
        return render_to_response(
            'doc/doc.html',
            {
                'version': version,
                'doc_list': doc_list,
            },
            context_instance=RequestContext(request))
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
                if path.exists(full_name):
                    files.append(
                        [
                            path.normpath(name),
                            datetime.fromtimestamp(path.getmtime(full_name)),
                            lang.lang
                        ])
                else:
                    files.append(['', '', lang.lang])
            if docv == '-':
                doc_list.append([doc, files])
            else:
                doc_list2.append([doc, files])
    return render_to_response(
        'doc/doc.html',
        {
            'version': version,
            'languages': languages,
            'bestlang': bestlang,
            'versions': versions,
            'doc_list': doc_list + doc_list2,
            'i18n': get_i18n_stats(),
            'doc_version': Release.objects.get(version=version).description,
        },
        context_instance=RequestContext(request))
