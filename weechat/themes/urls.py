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

"""URLs for "themes" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', 'weechat.themes.views.themes', name='themes'),
    url(r'^(?P<filter_name>(author))/(?P<filter_value>(.*))/$',
        'weechat.themes.views.themes',
        name='themes_filter'),
    url(r'^sort/(?P<sort_key>(name|version|added|updated))/$',
        'weechat.themes.views.themes',
        name='themes_sort'),
    url(r'^source/(?P<themeid>\d+)/$', 'weechat.themes.views.theme_source'),
    url(r'^source/(?P<themename>[a-zA-Z0-9_]+\.theme)\.html/$',
        'weechat.themes.views.theme_source',
        name='themes_source_name_html'),
    url(r'^add/$', 'weechat.themes.views.form_add',
        name='themes_add'),
    url(r'^update/$', 'weechat.themes.views.form_update',
        name='themes_update'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    url(r'^addok/$',
        TemplateView.as_view(template_name='themes/add_ok.html')),
    url(r'^adderror/$',
        TemplateView.as_view(template_name='themes/add_error.html')),
    url(r'^updateok/$',
        TemplateView.as_view(template_name='themes/update_ok.html')),
    url(r'^updateerror/$',
        TemplateView.as_view(template_name='themes/update_error.html')),
)
