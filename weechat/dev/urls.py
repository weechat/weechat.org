# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2014 Sébastien Helleu <flashcode@flashtux.org>
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

# URLs for menu "dev"

from django.conf.urls import *
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    (r'^$', 'weechat.dev.views.roadmap'),
    (r'^roadmap/$', 'weechat.dev.views.roadmap'),
    (r'^roadmap/all/$', 'weechat.dev.views.roadmap', {'allversions': True}),
    (r'^stats/$', 'weechat.dev.views.stats'),
    (r'^stats/(?P<stats>weechat|scripts|qweechat)/$',
     'weechat.dev.views.stats'),
    (r'^info/$', 'weechat.dev.views.info'),
    (r'^info/(?P<info>[a-zA-Z0-9_]*)/$', 'weechat.dev.views.info'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    (r'^support/$', TemplateView.as_view(template_name='dev/support.html')),
)
