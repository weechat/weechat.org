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

"""URLs for "scripts" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from weechat.scripts.views import (
    scripts as view_scripts,
    script_source as view_script_source,
    python3 as view_python3,
)

urlpatterns = [
    path('', view_scripts, name='scripts'),
    re_path(r'^(?P<filter_name>(tag|language|license|author))/'
            r'(?P<filter_value>(.*))/$',
            view_scripts, name='scripts_filter'),
    re_path(r'^sort/(?P<sort_key>(name|language|license|min_weechat|'
            r'max_weechat|author|added|updated))/$',
            view_scripts, name='scripts_sort'),
    re_path(r'^source/(?P<scriptid>\d+)/$', view_script_source,
            name='scripts_source_id'),
    re_path(r'^source/(?P<scriptname>[a-zA-Z0-9_.-]+)\.html/$',
            view_script_source, name='scripts_source_name_html'),
    re_path(r'^source/(?P<scriptname>[a-zA-Z0-9_.-]+)/$',
            view_script_source, name='scripts_source_name'),
    re_path(r'^source/(?P<scriptname>[a-zA-Z0-9_.-]+)\.html/$',
            view_script_source, name='scripts_source_name_html'),
    re_path(r'^source/(?P<scriptname>[a-zA-Z0-9_.-]+)/$',
            view_script_source, name='scripts_source_name'),
    path('add/', RedirectView.as_view(pattern_name='scripts')),
    path('update/', RedirectView.as_view(pattern_name='scripts')),
    path('pending/', RedirectView.as_view(pattern_name='scripts')),
    path('python3/', view_python3, name='scripts_python3'),
]
