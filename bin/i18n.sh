#!/bin/sh
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

DIR=$(cd $(dirname "$0"); pwd)

cd $DIR/../weechat || exit 1

chmod 644 locale/*/LC_MESSAGES/django.po

# generate new messages
django-admin makemessages -a

# edit locale if given as argument
if [ $# -gt 0 ]; then
    $EDITOR locale/$1/LC_MESSAGES/django.po || exit 1
fi

# compile messages
django-admin compilemessages
