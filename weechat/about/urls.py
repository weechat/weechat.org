#
# Copyright (C) 2003-2021 Sébastien Helleu <flashcode@flashtux.org>
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

from django.conf import settings
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from weechat.about.views import (
    screenshots as view_screenshots,
    history as view_history,
    about as view_about,
)

URL_ABOUT_EXTRA = getattr(settings, 'URL_ABOUT_EXTRA', 'extra')

urlpatterns = [
    path('', TemplateView.as_view(template_name='about/features.html'),
         name='about'),
    path('features/',
         TemplateView.as_view(template_name='about/features.html'),
         name='about_features'),
    path('interfaces/',
         TemplateView.as_view(template_name='about/interfaces.html'),
         name='about_interfaces'),
    path('screenshots/', view_screenshots, name='about_screenshots'),
    re_path(r'^screenshots/(?P<app>weechat|relay)/$', view_screenshots,
            name='about_screenshots_app'),
    re_path(r'^screenshots/(?P<app>weechat|relay)/'
            r'(?P<filename>[a-zA-Z0-9_\-.]*)/$',
            view_screenshots, name='about_screenshot'),
    path('screenshots/<str:filename>/', view_screenshots),
    path('history/', view_history, name='about_history'),
    path('support/', TemplateView.as_view(template_name='about/support.html'),
         name='about_support'),
    path('weechat.org/', view_about, name='about_weechat.org'),
    path(f'weechat.org/{URL_ABOUT_EXTRA}/', view_about,
         kwargs={'extra_info': True}),
]
