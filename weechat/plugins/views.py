# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2017 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for "scripts" menu."""

from datetime import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from weechat.common.path import files_path_join
from weechat.plugins.models import Plugin, PluginFormAdd, PluginFormUpdate, \
    get_language_from_extension

API_OLD = '0.2.6'
API_STABLE = '0.3.0'

# list of keys that are sorted by default using descending order
KEY_ORDER_BY_DESC = ['popularity', 'min_weechat', 'max_weechat', 'added',
                     'updated']

PYGMENTS_LEXER = {
    'pl': 'perl',
    'py': 'python',
    'rb': 'ruby',
    'lua': 'lua',
    'tcl': 'tcl',
    'scm': 'scheme',
    'js': 'javascript',
    'php': 'php',
}


def get_sort_key(sort_key):
    """Get sort keys to sort scripts (in SQL request)."""
    keys = sort_key.split(',')
    if 'name' not in keys:
        keys.append('name')
    for i, key in enumerate(keys):
        if key in KEY_ORDER_BY_DESC:
            keys[i] = '-%s' % key
    return keys


def get_highlighted_source(source, language):
    """Get source highlighted with pygments."""
    return highlight(source,
                     get_lexer_by_name(language, stripnl=True,
                                       encoding='utf-8'),
                     HtmlFormatter(cssclass='pygments', linenos='table'))


def scripts(request, api='stable', sort_key='popularity', filter_name='',
            filter_value=''):
    """Page with list of scripts."""

    def sort_by_popularity(item):
        return (-1 * item[1], item[0].lower())

    def sort_by_name(item):
        return item[0].lower()

    if api == 'legacy':
        plugin_list = Plugin.objects.filter(visible=1) \
            .filter(max_weechat=API_OLD).order_by(*get_sort_key(sort_key))
    else:
        plugin_list = Plugin.objects.filter(visible=1) \
            .filter(min_weechat__gte=API_STABLE) \
            .order_by(*get_sort_key(sort_key))
    if filter_name == 'tag':
        plugin_list = plugin_list \
            .filter(tags__regex=r'(^|,)%s($|,)' % filter_value)
    elif filter_name == 'language':
        plugin_list = plugin_list.filter(language=filter_value)
    elif filter_name == 'license':
        plugin_list = plugin_list.filter(license=filter_value)
    elif filter_name == 'author':
        plugin_list = plugin_list.filter(author=filter_value)
    languages = {}
    licenses = {}
    tags = {}
    for plugin in plugin_list:
        languages[plugin.language] = languages.get(plugin.language, 0) + 1
        licenses[plugin.license] = licenses.get(plugin.license, 0) + 1
        if plugin.tags:
            for tag in plugin.tagslist():
                tags[tag] = tags.get(tag, 0) + 1
    if request.COOKIES.get('script_filters_sort', '') == 'popularity':
        sort_function = sort_by_popularity
    else:
        sort_function = sort_by_name
    script_filters_displayed, script_filters_sort = (
        request.COOKIES.get('script_filters', '0_name').split('_'))
    return render(
        request,
        'plugins/list.html',
        {
            'plugin_list': plugin_list,
            'api': api,
            'sort_key': sort_key,
            'filter_name': filter_name,
            'filter_value': filter_value,
            'script_filters_displayed': int(script_filters_displayed),
            'script_filters_sort': script_filters_sort,
            'languages': sorted(languages.items(), key=sort_function),
            'licenses': sorted(licenses.items(), key=sort_function),
            'tags': sorted(tags.items(), key=sort_function),
        },
    )


def script_source(request, api='stable', scriptid='', scriptname=''):
    """Page with source of a script."""
    plugin = ''
    if scriptid:
        try:
            plugin = Plugin.objects.get(id=scriptid)
            with open(files_path_join(plugin.path(),
                                      plugin.name_with_extension()),
                      'rb') as _file:
                htmlsource = get_highlighted_source(_file.read(),
                                                    plugin.language)
        except:  # noqa: E722
            htmlsource = ''
    else:
        sname = scriptname
        sext = ''
        pos = sname.rfind('.')
        if pos > 0:
            sext = sname[pos+1:]
            sname = sname[0:pos]
        try:
            if api == 'legacy':
                plugin = Plugin.objects.get(
                    name=sname,
                    language=get_language_from_extension(sext),
                    max_weechat=API_OLD)
            else:
                plugin = Plugin.objects.get(
                    name=sname,
                    language=get_language_from_extension(sext),
                    min_weechat__gte=API_STABLE)
            with open(files_path_join(plugin.path(),
                                      plugin.name_with_extension()),
                      'rb') as _file:
                htmlsource = get_highlighted_source(_file.read(),
                                                    PYGMENTS_LEXER[sext])
        except:  # noqa: E722
            htmlsource = ''
    return render(
        request,
        'plugins/source.html',
        {
            'plugin': plugin,
            'htmlsource': htmlsource,
        },
    )


def form_add(request):
    """Page with form to add a script."""
    if request.method == 'POST':
        form = PluginFormAdd(request.POST, request.FILES)
        if form.is_valid():
            scriptfile = request.FILES['file']
            min_max = form.cleaned_data['min_max'].split(':')
            if min_max[0] == '-':
                min_max[0] = ''
            if min_max[1] == '-':
                min_max[1] = ''

            # add script in database
            now = datetime.now()
            plugin = Plugin(visible=False,
                            popularity=0,
                            name=form.cleaned_data['name'],
                            version=form.cleaned_data['version'],
                            url='',
                            language=form.cleaned_data['language'],
                            license=form.cleaned_data['license'],
                            desc_en=form.cleaned_data['description'],
                            requirements=form.cleaned_data['requirements'],
                            min_weechat=min_max[0],
                            max_weechat=min_max[1],
                            author=form.cleaned_data['author'],
                            mail=form.cleaned_data['mail'],
                            added=now,
                            updated=now)

            # write script in pending directory
            filename = files_path_join('scripts', 'pending1',
                                       plugin.name_with_extension())
            with open(filename, 'w') as _file:
                _file.write(scriptfile.read().replace('\r\n', '\n'))

            # send e-mail
            try:
                subject = ('WeeChat: new script %s' %
                           plugin.name_with_extension())
                body = (''
                        'Script      : %s\n'
                        'Version     : %s\n'
                        'Language    : %s\n'
                        'License     : %s\n'
                        'Description : %s\n'
                        'Requirements: %s\n'
                        'Min WeeChat : %s\n'
                        'Max WeeChat : %s\n'
                        'Author      : %s <%s>\n'
                        '\n'
                        'Comment:\n%s\n' %
                        (form.cleaned_data['name'],
                         form.cleaned_data['version'],
                         form.cleaned_data['language'],
                         form.cleaned_data['license'],
                         form.cleaned_data['description'],
                         form.cleaned_data['requirements'],
                         min_max[0],
                         min_max[1],
                         form.cleaned_data['author'],
                         form.cleaned_data['mail'],
                         form.cleaned_data['comment']))
                sender = '%s <%s>' % (form.cleaned_data['author'],
                                      form.cleaned_data['mail'])
                email = EmailMessage(subject, body, sender,
                                     settings.SCRIPTS_MAILTO)
                email.attach_file(filename)
                email.send()
            except:  # noqa: E722
                return HttpResponseRedirect('/scripts/adderror/')

            # save script in database
            plugin.save()

            return HttpResponseRedirect('/scripts/addok/')
    else:
        form = PluginFormAdd()
    return render(
        request,
        'plugins/add.html',
        {
            'form': form,
        },
    )


def form_update(request):
    """Page with form to update a script."""
    if request.method == 'POST':
        form = PluginFormUpdate(request.POST, request.FILES)
        if form.is_valid():
            scriptfile = request.FILES['file']
            plugin = Plugin.objects.get(id=form.cleaned_data['plugin'])

            # send e-mail
            try:
                subject = ('WeeChat: new release for script %s' %
                           plugin.name_with_extension())
                body = (''
                        'Script     : %s (%s)\n'
                        'New version: %s\n'
                        'Author     : %s <%s>\n'
                        '\n'
                        'Comment:\n%s\n' %
                        (plugin.name_with_extension(),
                         plugin.version_weechat(),
                         form.cleaned_data['version'],
                         form.cleaned_data['author'],
                         form.cleaned_data['mail'],
                         form.cleaned_data['comment']))
                sender = '%s <%s>' % (form.cleaned_data['author'],
                                      form.cleaned_data['mail'])
                email = EmailMessage(subject, body, sender,
                                     settings.SCRIPTS_MAILTO)
                email.attach(plugin.name_with_extension(),
                             scriptfile.read().replace('\r\n', '\n'),
                             'text/plain')
                email.send()
            except:  # noqa: E722
                return HttpResponseRedirect('/scripts/updateerror/')

            return HttpResponseRedirect('/scripts/updateok/')
    else:
        form = PluginFormUpdate()
    return render(
        request,
        'plugins/update.html',
        {
            'form': form,
        },
    )


def pending(request):
    """Page with scripts pending for approval."""
    plugin_list = Plugin.objects.filter(visible=0) \
        .filter(min_weechat__gte=API_STABLE).order_by('-added')
    return render(
        request,
        'plugins/pending.html',
        {
            'plugin_list': plugin_list,
        },
    )
