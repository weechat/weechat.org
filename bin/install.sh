#!/bin/sh
#
# Copyright (C) 2003-2016 Sébastien Helleu <flashcode@flashtux.org>
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

cd $DIR/.. || exit 1

if [ ! -f ./weechat/settings_local.py ]; then
    echo ""
    echo "--- Copy settings_local.template to settings_local.py"
    cp -v ./weechat/settings_local.template ./weechat/settings_local.py

    echo ""
    read -p "--- Change settings in settings_local.py (like databse)? (Y/n) " answer
    answer=${answer:-y}
    case $answer in
        y|Y) $EDITOR ./weechat/settings_local.py ;;
    esac
fi

echo ""
echo "--- Compiling messages"
./manage.py compilemessages

echo ""
echo "--- Creating database"
./manage.py syncdb

echo ""
echo "--- Loading fixtures in database"
./manage.py loaddata ./weechat/fixtures/*.json

echo ""
echo "--- Install OK!"
echo "--- You can run Django server with:  ./manage.py runserver"
