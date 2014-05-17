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

"""URLs for "about" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    'django.views.generic.simple',
    url(r'^(features/)?$',
        TemplateView.as_view(template_name='about/features.html')),
)

urlpatterns += patterns(
    '',
    url(r'^screenshots/$', 'weechat.about.views.screenshots'),
    url(r'^screenshots/(?P<filename>[a-zA-Z0-9_\-.]*)/$',
        'weechat.about.views.screenshots'),
    url(r'^history/$', 'weechat.about.views.history'),
    url(r'^donate/$', 'weechat.about.views.donate'),
    url(r'^donate/sort/(?P<sort_key>(date|top10))/$',
        'weechat.about.views.donate'),
    url(r'^donate/sort/(?P<sort_key>(date|top10))/'
        'view/(?P<view_key>[a-zA-Z0-9_]*)/$',
        'weechat.about.views.donate'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    url(r'^weechat\.org/$',
        TemplateView.as_view(template_name='about/weechat.org.html')),
)
