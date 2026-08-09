# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""URLs for "scripts" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from weechat.scripts.views import (
    python3 as view_python3,
)
from weechat.scripts.views import (
    script_source as view_script_source,
)
from weechat.scripts.views import (
    scripts as view_scripts,
)

urlpatterns = [
    path('', view_scripts, name='scripts'),
    re_path(r'^(?P<filter_name>(tag|language|license|author))/'
            r'(?P<filter_value>([^/]+))/$',
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
