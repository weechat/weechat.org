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

"""Some i18n useful functions."""

from io import open

from weechat.common.path import project_path_join


def i18n_autogen(app, name, strings):
    """Create a file '_i18n_xxx.py' with strings to translate."""
    # build content of file
    content = [
        '# This file is auto-generated after changes in database, '
        'DO NOT EDIT!',
        '',
        f'"""Translations for {app}/{name}."""',
        '',
        '# flake8: noqa',
        '# pylint: disable=line-too-long,too-many-statements',
    ]
    if strings:
        content += [
            '',
            'from django.utils.translation import gettext_noop',
            '',
            '',
            f'def __i18n_{app}_{name}():',
            f'    """Translations for {app}/{name}."""',
        ]
        done = set()
        for string in sorted(strings):
            if isinstance(string, tuple):
                # if type is tuple of 2 strings: use the second as note for
                # translators
                (message, translators) = (string[0], string[1])
            else:
                # single string (no note for translators)
                (message, translators) = (string, None)
            # add string if not already done
            if message not in done:
                if translators:
                    content.append(f'    # Translators: {translators}')
                message = (message
                           .replace('\\', '\\\\')
                           .replace('"', '\\"')
                           .replace('\r\n', '\\n'))
                content.append(f'    gettext_noop("{message}")')
                done.add(message)
    content.append('')
    # write file
    filename = project_path_join(app, f'_i18n_{name}.py')
    with open(filename, 'w', encoding='utf-8') as _file:
        data = '\n'.join(content)
        if hasattr(data, 'decode') and isinstance(data, str):
            data = data.decode('utf-8')
        _file.write(data)
