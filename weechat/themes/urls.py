# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""URLs for "themes" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path
from django.views.generic.base import TemplateView

from weechat.themes.views import (
    form_add as view_form_add,
)
from weechat.themes.views import (
    form_update as view_form_update,
)
from weechat.themes.views import (
    theme_source as view_theme_source,
)
from weechat.themes.views import (
    themes as view_themes,
)

urlpatterns = [
    path('', view_themes, name='themes'),
    re_path(r'^(?P<filter_name>(author))/(?P<filter_value>([^/]+))/$',
            view_themes, name='themes_filter'),
    re_path(r'^sort/(?P<sort_key>(name|version|added|updated))/$',
            view_themes, name='themes_sort'),
    re_path(r'^source/(?P<themeid>\d+)/$', view_theme_source),
    re_path(r'^source/(?P<themename>[a-zA-Z0-9_]+\.theme)\.html/$',
            view_theme_source, name='themes_source_name_html'),
    path('add/', view_form_add, name='themes_add'),
    path('update/', view_form_update, name='themes_update'),
    path('addok/', TemplateView.as_view(template_name='themes/add_ok.html')),
    path('adderror/',
         TemplateView.as_view(template_name='themes/add_error.html')),
    path('updateok/',
         TemplateView.as_view(template_name='themes/update_ok.html')),
    path('updateerror/',
         TemplateView.as_view(template_name='themes/update_error.html')),
]
