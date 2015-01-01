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

"""URLs for "scripts" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', 'weechat.plugins.views.scripts', name='scripts'),
    url(r'^(?P<api>(old|stable))/$', 'weechat.plugins.views.scripts',
        name='scripts_api'),
    url(r'^(?P<api>(old|stable))/'
        r'(?P<filter_name>(tag|language|license|author))/'
        r'(?P<filter_value>(.*))/$',
        'weechat.plugins.views.scripts',
        name='scripts_api_filter'),
    url(r'^(?P<api>(old|stable))/sort/(?P<sort_key>(name|language|license|'
        r'min_weechat|max_weechat|author|added|updated))/$',
        'weechat.plugins.views.scripts',
        name='scripts_api_sort'),
    url(r'^source/(?P<scriptid>\d+)/$', 'weechat.plugins.views.script_source',
        name='scripts_source_id'),
    url(r'^source/(?P<api>(old|stable))/(?P<scriptname>[a-zA-Z0-9_.-]+)'
        r'\.html/$',
        'weechat.plugins.views.script_source',
        name='scripts_source_api_name_html'),
    url(r'^source/(?P<api>(old|stable))/(?P<scriptname>[a-zA-Z0-9_.-]+)/$',
        'weechat.plugins.views.script_source',
        name='scripts_source_api_name'),
    url(r'^source/(?P<scriptname>[a-zA-Z0-9_.-]+)\.html/$',
        'weechat.plugins.views.script_source', {'api': 'stable'},
        name='scripts_source_name_html'),
    url(r'^source/(?P<scriptname>[a-zA-Z0-9_.-]+)/$',
        'weechat.plugins.views.script_source', {'api': 'stable'},
        name='scripts_source_name'),
    url(r'^add/$', 'weechat.plugins.views.form_add',
        name='scripts_add'),
    url(r'^update/$', 'weechat.plugins.views.form_update',
        name='scripts_update'),
    url(r'^pending/$', 'weechat.plugins.views.pending',
        name='scripts_pending'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    url(r'^addok/$',
        TemplateView.as_view(template_name='plugins/add_ok.html')),
    url(r'^adderror/$',
        TemplateView.as_view(template_name='plugins/add_error.html')),
    url(r'^updateok/$',
        TemplateView.as_view(template_name='plugins/update_ok.html')),
    url(r'^updateerror/$',
        TemplateView.as_view(template_name='plugins/update_error.html')),
)
