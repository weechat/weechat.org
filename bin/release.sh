#!/bin/sh
#
# SPDX-FileCopyrightText: 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
# Manage release: add/update a release, set stable/devel version.
#
# Syntax:
#   ./add_version.sh <action> <project> <version>
#
#     action: one of: "add", "stable", "devel"
#     project: project name (eg: "weechat", "weechat-relay", etc.)
#     version: version (eg: "4.0.0", "4.1.0-dev")
#
# Actions:
#   - add: add release + packages (.tar.gz + .tar.xz).
#          note: the files must exist in src directory, otherwise checksums
#                will not be set.
#   - stable: set the stable release
#   - devel: set the devel release
#
# Examples:
#   ./release.sh add weechat 4.0.0
#   ./release.sh stable weechat 4.0.0
#   ./release.sh devel weechat 4.1.0-dev
#

set -o errexit

DIR=$(cd "$(dirname "$0")"; pwd)

if [ $# -lt 2 ]; then
    echo >&2
    echo >&2 "Syntax: $0 <action> <project> <version>"
    echo >&2
    echo >&2 "  action  \"add\", \"stable\" or \"devel\""
    echo >&2 "  project  project name (eg: \"weechat\")"
    echo >&2 "  version  version (eg: \"4.0.0\", \"4.1.0-dev\")"
    echo >&2
    exit 1
fi

ACTION="$1"
PROJECT="$2"
VERSION="$3"

"${DIR}/../manage.py" shell <<EOF
from weechat.download.models import release_action
release_action("${ACTION}", "${PROJECT}", "${VERSION}")
EOF
