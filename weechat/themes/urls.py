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

"""URLs for "themes" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path
from django.views.generic.base import TemplateView

from weechat.themes.views import (
    themes as view_themes,
    theme_source as view_theme_source,
    form_add as view_form_add,
    form_update as view_form_update,
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
