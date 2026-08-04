# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
