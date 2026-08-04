#!/bin/sh
#
# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
