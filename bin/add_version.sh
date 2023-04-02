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
# Add a WeeChat version in database:
#  1. set stable version + date (today)
#  2. set devel version + date (next version)
#  3. add packages (.tar.gz + .tar.xz)
#     note: files must exist in files/src directory,
#           otherwise checksum will not be set
#
# Syntax:
#   ./add_version.sh <version>
#
# Example:
#   ./add_version.sh 4.0.0
#

set -o errexit

DIR=$(cd "$(dirname "$0")"; pwd)

if [ $# -lt 1 ]; then
    echo "Syntax: $0 <version>"
    exit 1
fi

VERSION="$1"
NEXT_DEVEL=$(echo "$VERSION" | awk -F. '{$(NF-1) = $(NF-1) + 1; $NF = 0; print}' OFS=.)
NEXT_DEVEL_FULL="${NEXT_DEVEL}-dev"

echo "Setting: stable=${VERSION}, devel=${NEXT_DEVEL_FULL}"
echo "Creating packages for WeeChat ${VERSION}: weechat-${VERSION}.tar.{gz,xz}"

"${DIR}/../manage.py" shell <<EOF
from datetime import date
from weechat.download.models import Release, Package, Type
v_stable = Release.objects.get(version="stable")
v_stable.description = "${VERSION}"
v_stable.date = date.today()
v_stable.security_issues_fixed = 0
v_stable.securityfix = ""
v_stable.save()
v_new = Release.objects.get(version="${VERSION}")
v_new.date = date.today()
v_new.security_issues_fixed = 0
v_new.securityfix = ""
v_new.save()
v_devel = Release.objects.get(version="devel")
v_devel.description = "${NEXT_DEVEL_FULL}"
v_devel.date = Release.objects.get(version="${NEXT_DEVEL}").date
v_devel.security_issues_fixed = 0
v_devel.securityfix = ""
v_devel.save()
version = Release.objects.get(version="${VERSION}")
for ext in ("gz", "xz"):
    Package.objects.filter(filename=f"weechat-${VERSION}.tar.{ext}").delete()
    pkg = Package(
        version=version,
        type=Type.objects.get(type=f"src1-{ext}"),
        filename=f"weechat-${VERSION}.tar.{ext}"
    )
    pkg.save()
EOF
