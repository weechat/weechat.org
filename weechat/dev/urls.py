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

"""URLs for "dev" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path

from weechat.dev.views import (
    roadmap as view_roadmap,
    stats_repo as view_stats_repo,
    info as view_info,
)

urlpatterns = [
    path('', view_roadmap, name='dev'),
    path('roadmap/', view_roadmap, name='dev_roadmap'),
    re_path(r'^roadmap/(?P<versions>future|released)/$', view_roadmap,
            name='dev_roadmap_versions'),
    path('stats/', view_stats_repo, name='dev_stats'),
    re_path(r'^stats/(?P<stats>weechat|weechat-relay|scripts|qweechat'
            r'|weechat\.org)/$',
            view_stats_repo, name='dev_stats_git'),
    path('info/', view_info, name='dev_info'),
    re_path(r'^info/(?P<name>[a-zA-Z0-9_]*)/$', view_info,
            name='dev_info_name'),
]
