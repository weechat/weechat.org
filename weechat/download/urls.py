# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2020 Sébastien Helleu <flashcode@flashtux.org>
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

"""URLs for "download" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import url

from weechat.debian.views import repos as view_repos
from weechat.download.views import (
    packages as view_packages,
    package_checksums as view_package_checksums,
    release as view_release,
)

urlpatterns = [
    url(r'^$', view_packages, name='download'),
    url(r'^debian/$', view_repos, {'active': 'active'},
        name='download_debian'),
    url(r'^debian/(?P<active>(active|all))/$', view_repos,
        name='download_debian_active'),
    url(r'^debian/(?P<active>(active|all))/(?P<files>[a-zA-Z0-9.]*)/$',
        view_repos),
    url(r'^release/$', view_release, name='download_release'),
    url(r'^checksums/weechat-(?P<version>[a-zA-Z0-9.]*)-'
        r'(?P<checksum_type>[a-zA-Z0-9]*).txt/$',
        view_package_checksums, name='package_checksums'),
    url(r'^(?P<version>[a-zA-Z0-9.]*)/$', view_packages,
        name='download_version'),
]
