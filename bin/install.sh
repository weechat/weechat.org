#!/bin/sh
#
# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -o errexit

DIR=$(cd "$(dirname "$0")"; pwd)

cd "$DIR/.."

echo ""
echo "--- Installing Python dependencies"
uv sync --locked

echo ""
echo "--- Compiling messages"
uv run python manage.py compilemessages

echo ""
echo "--- Creating database"
uv run python manage.py migrate --run-syncdb

echo ""
echo "--- Loading fixtures in database"
uv run python manage.py loaddata ./weechat/fixtures/*.json

echo ""
echo "--- Install OK!"
echo ""
echo "--- You can run Django server with:  ./test.sh"
