# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""URLs for "dev" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path

from weechat.dev.views import (
    info as view_info,
)
from weechat.dev.views import (
    roadmap as view_roadmap,
)
from weechat.dev.views import (
    stats_repo as view_stats_repo,
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
    re_path(r'^info/(?P<name>[a-zA-Z0-9_]+)/$', view_info,
            name='dev_info_name'),
]
