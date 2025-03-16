#
# Copyright (C) 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for "themes" menu."""

# pylint: disable=no-name-in-module

from datetime import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from weechat.common.path import files_path_join
from weechat.download.models import Release
from weechat.themes.models import Theme, ThemeFormAdd, ThemeFormUpdate

# list of keys that are sorted by default using descending order
KEY_ORDER_BY_DESC = ['version', 'added', 'updated']


def themes(request, sort_key='updated', filter_name='', filter_value=''):
    """Page with list of themes."""
    if sort_key in KEY_ORDER_BY_DESC:
        sort_key = f'-{sort_key}'
    theme_list = Theme.objects.filter(visible=1).order_by(sort_key)
    if filter_name == 'author':
        theme_list = theme_list.filter(author=filter_value)
    return render(
        request,
        'themes/list.html',
        {
            'theme_list': theme_list,
            'sort_key': sort_key,
            'filter_name': filter_name,
            'filter_value': filter_value,
        },
    )


def theme_source(request, themeid=None, themename=None):
    """Page with source of a theme."""
    if themeid:
        theme = get_object_or_404(Theme, id=themeid)
    else:
        theme = get_object_or_404(Theme, name=themename)
    try:
        with open(files_path_join(theme.path(), theme.name), 'rb') as _file:
            html_source = highlight(_file.read(),
                                    get_lexer_by_name('ini', stripnl=True,
                                                      encoding='utf-8'),
                                    HtmlFormatter(cssclass='pygments',
                                                  linenos='table'))
    except Exception as exc:  # noqa: E722  pylint: disable=bare-except
        raise Http404 from exc
    return render(
        request,
        'themes/source.html',
        {
            'weechat_theme': theme,
            'html_source': mark_safe(html_source),
        },
    )


def get_theme_content(theme_file):
    """Get content of theme file (replace "\r\n" by "\n")."""
    content = theme_file.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    return content.replace('\r\n', '\n')


def form_add(request):
    """Page with form to add a theme."""
    if request.method == 'POST':
        form = ThemeFormAdd(request.POST, request.FILES)
        if form.is_valid():
            themefile = request.FILES['themefile']

            # get properties
            content = get_theme_content(themefile)
            props = Theme.get_props(content)

            # add theme in database
            now = datetime.now()
            theme = Theme(visible=False,
                          name=props['name'],
                          version=props['weechat'],
                          desc=form.cleaned_data['description'],
                          author=form.cleaned_data['author'],
                          mail=form.cleaned_data['mail'],
                          added=now,
                          updated=now)

            # write theme in pending directory
            filename = files_path_join('themes', 'pending', theme.name)
            with open(filename, 'w', encoding='utf-8') as _file:
                _file.write(content)

            # send e-mail
            if settings.THEMES_MAILTO:
                try:
                    subject = f'WeeChat: new theme {theme.name}'
                    sender = (f'{form.cleaned_data["author"]} '
                              f'<{form.cleaned_data["mail"]}>')
                    body = (
                        f'Theme      : {props["name"]}\n'
                        f'Version    : {props["weechat"]}\n'
                        f'Description: {form.cleaned_data["description"]}\n'
                        f'Author     : {sender}\n'
                        f'Comment    :\n{form.cleaned_data["comment"]}\n'
                    )
                    email = EmailMessage(subject, body, sender,
                                         settings.THEMES_MAILTO)
                    email.attach_file(filename)
                    email.send()
                except:  # noqa: E722  pylint: disable=bare-except
                    return HttpResponseRedirect('/themes/adderror/')

            # save theme in database
            theme.save()

            return HttpResponseRedirect('/themes/addok/')
    else:
        form = ThemeFormAdd()
    try:
        stable_version = Release.objects.get(project__name='weechat',
                                             version='stable').description
        release_stable = Release.objects.get(project__name='weechat',
                                             version=stable_version)
    except ObjectDoesNotExist:
        release_stable = None
    return render(
        request,
        'themes/add.html',
        {
            'release_stable': release_stable,
            'form': form,
        },
    )


def form_update(request):
    """Page with form to update a theme."""
    if request.method == 'POST':
        form = ThemeFormUpdate(request.POST, request.FILES)
        if form.is_valid():
            themefile = request.FILES['themefile']
            theme = Theme.objects.get(id=form.cleaned_data['theme'])

            # get properties
            content = get_theme_content(themefile)
            props = Theme.get_props(content)

            # send e-mail
            if not settings.THEMES_MAILTO:
                return HttpResponseRedirect('/themes/updateerror/')
            try:
                subject = f'WeeChat: new version of theme {theme.name}'
                sender = (f'{form.cleaned_data["author"]} '
                          f'<{form.cleaned_data["mail"]}>')
                body = (f'Theme      : {theme.name}\n'
                        f'Version    : {theme.version}\n'
                        f'New version: {props["weechat"]}\n'
                        f'Author     : {sender}\n'
                        f'Comment    :\n{form.cleaned_data["comment"]}\n')
                email = EmailMessage(subject, body, sender,
                                     settings.THEMES_MAILTO)
                email.attach(theme.name, content, 'text/plain')
                email.send()
            except:  # noqa: E722  pylint: disable=bare-except
                return HttpResponseRedirect('/themes/updateerror/')

            return HttpResponseRedirect('/themes/updateok/')
    else:
        form = ThemeFormUpdate()
    return render(
        request,
        'themes/update.html',
        {
            'form': form,
        },
    )
