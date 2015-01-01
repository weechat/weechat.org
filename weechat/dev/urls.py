# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2015 Sébastien Helleu <flashcode@flashtux.org>
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

"""URLs for "dev" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', 'weechat.dev.views.roadmap', name='dev'),
    url(r'^roadmap/$', 'weechat.dev.views.roadmap', name='dev_roadmap'),
    url(r'^roadmap/all/$', 'weechat.dev.views.roadmap', {'allversions': True},
        name='dev_roadmap_all'),
    url(r'^stats/$', 'weechat.dev.views.stats_repo', name='dev_stats'),
    url(r'^stats/(?P<stats>weechat|scripts|qweechat|weechat\.org)/$',
        'weechat.dev.views.stats_repo', name='dev_stats_git'),
    url(r'^info/$', 'weechat.dev.views.info', name='dev_info'),
    url(r'^info/(?P<name>[a-zA-Z0-9_]*)/$', 'weechat.dev.views.info',
        name='dev_info_name'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    url(r'^support/$', TemplateView.as_view(template_name='dev/support.html'),
        name='dev_support'),
)
