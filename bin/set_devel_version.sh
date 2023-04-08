#!/bin/sh
#
# Copyright (C) 2003-2023 Sébastien Helleu <flashcode@flashtux.org>
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

#
# Set development version in database for "devel" release:
#   - version = the one provided
#   - date = date of this release (unchanged if release is not found)
#
# Syntax:
#   ./set_devel_version.sh <version>
#
# Example:
#   ./set_devel_version.sh 4.1.0-dev
#

set -o errexit

DIR=$(cd "$(dirname "$0")"; pwd)

if [ $# -lt 1 ]; then
    echo "Syntax: $0 <version>"
    exit 1
fi

VERSION_FULL="$1"
VERSION=$(echo "${VERSION_FULL}" | cut -d"-" -f1)

echo "Setting: devel=${VERSION_FULL}"

"${DIR}/../manage.py" shell <<EOF
from weechat.download.models import Release
v_devel = Release.objects.get(version="devel")
v_devel.description = "${VERSION_FULL}"
if Release.objects.filter(version="${VERSION}").exists():
    v_devel.date = Release.objects.get(version="${VERSION}").date
v_devel.save()
EOF
