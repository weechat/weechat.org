#!/bin/sh
#
# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -o errexit

DIR=$(cd "$(dirname "$0")"; pwd)

cd "${DIR}/../weechat"

chmod 644 locale/*/LC_MESSAGES/django.po

# generate new messages
django-admin makemessages -a

# edit locale if given as argument
if [ $# -gt 0 ]; then
    "$EDITOR" "locale/$1/LC_MESSAGES/django.po"
fi

# compile messages
django-admin compilemessages
