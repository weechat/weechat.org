# -*- coding: utf-8 -*-
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

"""URLs for "download" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'weechat.download.views.packages', name='download'),
    url(r'^debian/$', 'weechat.debian.views.repos', name='download_debian'),
    url(r'^debian/(?P<files>[a-zA-Z0-9.]*)/$', 'weechat.debian.views.repos'),
    url(r'^release/$', 'weechat.download.views.release',
        name='download_release'),
    url(r'^security/$', 'weechat.download.views.security',
        name='download_security'),
    url(r'^(?P<version>[a-zA-Z0-9.]*)/$', 'weechat.download.views.packages',
        name='download_version'),
]
