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

"""Views for "scripts" menu."""

from datetime import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from weechat.common.path import files_path_join
from weechat.download.models import Release
from weechat.scripts.models import (
    Script,
    ScriptFormAdd,
    ScriptFormUpdate,
    get_language_from_extension,
)

# list of keys that are sorted by default using descending order
KEY_ORDER_BY_DESC = (
    'popularity',
    'min_weechat',
    'max_weechat',
    'added',
    'updated',
)

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
            keys[i] = f'-{key}'
    return keys


def get_highlighted_source(source, language):
    """Get source highlighted with pygments."""
    return highlight(source,
                     get_lexer_by_name(language, stripnl=True,
                                       encoding='utf-8'),
                     HtmlFormatter(cssclass='pygments', linenos='table'))


def scripts(request, sort_key='popularity', filter_name='', filter_value=''):
    """Page with list of scripts."""
    # pylint: disable=too-many-locals,too-many-branches

    def sort_by_popularity(item):
        return (-1 * item[1], item[0].lower())

    def sort_by_name(item):
        return item[0].lower()

    script_list = (Script.objects.filter(approved=True)
                   .order_by(*get_sort_key(sort_key)))
    if filter_name == 'tag':
        script_list = (script_list
                       .filter(tags__regex=rf'(^|,){filter_value}($|,)'))
    elif filter_name == 'language':
        if filter_value == 'python2-compatible':
            script_list = (script_list
                           .filter(language='python')
                           .filter(tags__regex=r'(^|,)py2($|,)'))
        elif filter_value == 'python2-only':
            script_list = (script_list
                           .filter(language='python')
                           .exclude(tags__regex=r'(^|,)py3($|,)'))
        elif filter_value == 'python3-compatible':
            script_list = (script_list
                           .filter(language='python')
                           .filter(tags__regex=r'(^|,)py3($|,)'))
        elif filter_value == 'python3-only':
            script_list = (script_list
                           .filter(language='python')
                           .exclude(tags__regex=r'(^|,)py2($|,)'))
        else:
            script_list = script_list.filter(language=filter_value)
    elif filter_name == 'license':
        script_list = script_list.filter(license=filter_value)
    elif filter_name == 'author':
        script_list = script_list.filter(author=filter_value)
    languages = {}
    licenses = {}
    tags = {}
    for script in script_list:
        languages[script.language] = languages.get(script.language, 0) + 1
        if script.language == 'python':
            py2_ok = script.is_py2_ok()
            py3_ok = script.is_py3_ok()
            if py2_ok:
                languages['python2-compatible'] = \
                    languages.get('python2-compatible', 0) + 1
                if not py3_ok:
                    languages['python2-only'] = \
                        languages.get('python2-only', 0) + 1
            if py3_ok:
                languages['python3-compatible'] = \
                    languages.get('python3-compatible', 0) + 1
                if not py2_ok:
                    languages['python3-only'] = \
                        languages.get('python3-only', 0) + 1
        licenses[script.license] = licenses.get(script.license, 0) + 1
        if script.tags:
            for tag in script.tagslist():
                tags[tag] = tags.get(tag, 0) + 1
    script_filters_displayed, script_filters_sort = (
        request.COOKIES.get('script_filters', '0_name').split('_'))
    if script_filters_sort == 'popularity':
        sort_function = sort_by_popularity
    else:
        sort_function = sort_by_name
    return render(
        request,
        'scripts/list.html',
        {
            'script_list': script_list,
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


def script_source(request, scriptid='', scriptname=''):
    """Page with source of a script."""
    script = None
    if scriptid:
        script = get_object_or_404(Script, id=scriptid)
        try:
            with open(files_path_join(script.path(),
                                      script.name_with_extension()),
                      'rb') as _file:
                htmlsource = get_highlighted_source(_file.read(),
                                                    script.language)
        except:  # noqa: E722  pylint: disable=bare-except
            raise Http404
    else:
        sname = scriptname
        sext = ''
        pos = sname.rfind('.')
        if pos > 0:
            sext = sname[pos+1:]
            sname = sname[0:pos]
        script = get_object_or_404(
            Script,
            name=sname,
            language=get_language_from_extension(sext),
        )
        try:
            with open(files_path_join(script.path(),
                                      script.name_with_extension()),
                      'rb') as _file:
                htmlsource = get_highlighted_source(_file.read(),
                                                    PYGMENTS_LEXER[sext])
        except:  # noqa: E722  pylint: disable=bare-except
            raise Http404
    return render(
        request,
        'scripts/source.html',
        {
            'script': script,
            'htmlsource': htmlsource,
        },
    )


def get_script_content(script_file):
    """Get content of script file (replace "\r\n" by "\n")."""
    content = script_file.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    return content.replace('\r\n', '\n')


def form_add(request):
    """Page with form to add a script."""
    if request.method == 'POST':
        form = ScriptFormAdd(request.POST, request.FILES)
        if form.is_valid():
            scriptfile = request.FILES['file']

            # add script in database
            now = datetime.now()
            script = Script(approved=False,
                            popularity=0,
                            name=form.cleaned_data['name'],
                            version=form.cleaned_data['version'],
                            url='',
                            language=form.cleaned_data['language'],
                            license=form.cleaned_data['license'],
                            desc_en=form.cleaned_data['description'],
                            requirements=form.cleaned_data['requirements'],
                            min_weechat=form.cleaned_data['min_weechat'],
                            author=form.cleaned_data['author'],
                            mail=form.cleaned_data['mail'],
                            added=now,
                            updated=now)

            # write script in pending directory
            filename = files_path_join('scripts', 'pending1',
                                       script.name_with_extension())
            with open(filename, 'w') as _file:
                _file.write(get_script_content(scriptfile))

            # send e-mail
            if settings.SCRIPTS_MAILTO:
                try:
                    subject = (f'WeeChat: new script '
                               f'{script.name_with_extension()}')
                    sender = (f'{form.cleaned_data["author"]} '
                              f'<{form.cleaned_data["mail"]}>')
                    body = (
                        f'Script      : {form.cleaned_data["name"]}\n'
                        f'Version     : {form.cleaned_data["version"]}\n'
                        f'Language    : {form.cleaned_data["language"]}\n'
                        f'License     : {form.cleaned_data["license"]}\n'
                        f'Description : {form.cleaned_data["description"]}\n'
                        f'Requirements: {form.cleaned_data["requirements"]}\n'
                        f'Min WeeChat : {form.cleaned_data["min_weechat"]}\n'
                        f'Author      : {sender}>\n'
                        f'\n'
                        f'Comment:\n{form.cleaned_data["comment"]}\n'
                    )
                    email = EmailMessage(subject, body, sender,
                                         settings.SCRIPTS_MAILTO)
                    email.attach_file(filename)
                    email.send()
                except:  # noqa: E722  pylint: disable=bare-except
                    return HttpResponseRedirect('/scripts/adderror/')

            # save script in database
            script.save()

            return HttpResponseRedirect('/scripts/addok/')
    else:
        form = ScriptFormAdd()
    return render(
        request,
        'scripts/add.html',
        {
            'form': form,
        },
    )


def form_update(request):
    """Page with form to update a script."""
    if request.method == 'POST':
        form = ScriptFormUpdate(request.POST, request.FILES)
        if form.is_valid():
            scriptfile = request.FILES['file']
            script = Script.objects.get(id=form.cleaned_data['script'])

            # send e-mail
            if not settings.SCRIPTS_MAILTO:
                return HttpResponseRedirect('/scripts/updateerror/')
            try:
                subject = (f'WeeChat: new release for script '
                           f'{script.name_with_extension()}')
                sender = (f'{form.cleaned_data["author"]} '
                          f'<{form.cleaned_data["mail"]}>')
                body = (f'Script     : {script.name_with_extension()} '
                        f'({script.version_weechat()})\n'
                        f'New version: {form.cleaned_data["version"]}\n'
                        f'Author     : {sender}\n'
                        f'\n'
                        f'Comment:\n{form.cleaned_data["comment"]}\n')
                email = EmailMessage(subject, body, sender,
                                     settings.SCRIPTS_MAILTO)
                email.attach(script.name_with_extension(),
                             get_script_content(scriptfile),
                             'text/plain')
                email.send()
            except:  # noqa: E722  pylint: disable=bare-except
                return HttpResponseRedirect('/scripts/updateerror/')

            return HttpResponseRedirect('/scripts/updateok/')
    else:
        form = ScriptFormUpdate()
    return render(
        request,
        'scripts/update.html',
        {
            'form': form,
        },
    )


def pending(request):
    """Page with scripts pending for approval."""
    script_list = Script.objects.filter(approved=False).order_by('-added')
    return render(
        request,
        'scripts/pending.html',
        {
            'script_list': script_list,
        },
    )


def python3(request):
    """Page with Python 3 transition."""
    v037_date = Release.objects.get(version='0.3.7').date
    v037_date = datetime(
        year=v037_date.year,
        month=v037_date.month,
        day=v037_date.day,
    )
    status_list = []
    # status when the transition started
    status_list.append({
        'date': datetime(2018, 6, 3),
        'scripts': 347,
        'python_scripts': 216,
        'scripts_ok': 43,
        'scripts_remaining': 173,
    })
    # status on 2019-07-01 (WeeChat is built with Python 3 by default)
    status_list.append({
        'date': datetime(2019, 7, 1),
        'scripts': 362,
        'python_scripts': 226,
        'scripts_ok': 96,
        'scripts_remaining': 130,
    })
    # status on 2020-01-01 (initial end of transition)
    status_list.append({
        'date': datetime(2020, 1, 1),
        'scripts': 364,
        'python_scripts': 228,
        'scripts_ok': 125,
        'scripts_remaining': 103,
    })
    # status on 2020-05-01 (end of transition)
    status_list.append({
        'date': datetime(2020, 5, 1),
        'scripts': 364,
        'python_scripts': 228,
        'scripts_ok': 129,
        'scripts_remaining': 99,
    })
    # status today
    scripts_list = Script.objects.filter(approved=True).count()
    python_scripts = (Script.objects.filter(approved=True)
                      .filter(language='python')
                      .count())
    scripts_ok = (Script.objects.filter(approved=True)
                  .filter(language='python')
                  .filter(tags__regex=r'(^|,)py3($|,)')
                  .count())
    scripts_remaining = python_scripts - scripts_ok
    status_list.append({
        'date': datetime.now(),
        'today': True,
        'scripts': scripts_list,
        'python_scripts': python_scripts,
        'scripts_ok': scripts_ok,
        'scripts_remaining': scripts_remaining,
    })
    # compute percentages and flag "future"
    now = datetime.now()
    for status in status_list:
        status['python_scripts_percent'] = (
            (status['python_scripts'] * 100) // status['scripts']
        )
        status['scripts_ok_percent'] = (
            (status['scripts_ok'] * 100) // status['python_scripts']
        )
        status['scripts_remaining_percent'] = (
            100 - status['scripts_ok_percent']
        )
        status['future'] = status['date'] > now
    return render(
        request,
        'scripts/python3.html',
        {
            'python3_date': datetime(2008, 12, 3),
            'v037_date': v037_date,
            'roadmap_start': datetime(2018, 6, 3),
            'roadmap_email': datetime(2018, 6, 16),
            'roadmap_new_py3': datetime(2018, 7, 1),
            'roadmap_all_py3': datetime(2018, 9, 1),
            'roadmap_weechat_py3': datetime(2019, 7, 1),
            'roadmap_initial_end': datetime(2020, 1, 1),
            'roadmap_end': datetime(2020, 5, 1),
            'status_list': status_list,
        },
    )
