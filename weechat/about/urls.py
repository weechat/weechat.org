# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2018 Sébastien Helleu <flashcode@flashtux.org>
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

"""URLs for "about" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import url
from django.views.generic.base import TemplateView

from weechat.about.views import (
    screenshots as view_screenshots,
    history as view_history,
)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='about/features.html'),
        name='about'),
    url(r'^features/$',
        TemplateView.as_view(template_name='about/features.html'),
        name='about_features'),
    url(r'^interfaces/$',
        TemplateView.as_view(template_name='about/interfaces.html'),
        name='about_interfaces'),
    url(r'^screenshots/$', view_screenshots, name='about_screenshots'),
    url(r'^screenshots/(?P<app>weechat|relay)/$', view_screenshots,
        name='about_screenshots_app'),
    url(r'^screenshots/(?P<app>weechat|relay)/'
        r'(?P<filename>[a-zA-Z0-9_\-.]*)/$',
        view_screenshots, name='about_screenshot'),
    url(r'^screenshots/(?P<filename>[a-zA-Z0-9_\-.]*)/$', view_screenshots),
    url(r'^history/$', view_history, name='about_history'),
    url(r'^support/$',
        TemplateView.as_view(template_name='about/support.html'),
        name='about_support'),
    url(r'^weechat\.org/$',
        TemplateView.as_view(template_name='about/weechat.org.html'),
        name='about_weechat.org'),
]
