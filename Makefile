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

all: check

check: gettext lint

lint: flake8 pylint

gettext:
	msgcheck weechat/locale/*/LC_MESSAGES/django.po

flake8:
	flake8 weechat --count --max-line-length=88 --select=E9,F63,F7,F82 --exclude=migrations --show-source --statistics
	flake8 weechat --count --max-line-length=88 --exclude=migrations --exit-zero --max-complexity=10 --statistics

pylint:
	pylint --load-plugins pylint_django --disable=fixme,duplicate-code,django-not-configured --ignore=migrations weechat
