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

all: check

check: gettext lint

lint: flake8 pylint

gettext:
	msgcheck weechat/locale/*/LC_MESSAGES/django.po

flake8:
	flake8 weechat --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 weechat --count --exit-zero --max-complexity=10 --statistics

pylint:
	pylint --load-plugins pylint_django --disable=fixme,duplicate-code,django-not-configured weechat
