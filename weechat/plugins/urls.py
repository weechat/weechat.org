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

# URLs for menu "scripts"

from django.conf.urls import *
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    (r'^$', 'weechat.plugins.views.scripts'),
    (r'^(?P<api>(old|stable))/$', 'weechat.plugins.views.scripts'),
    (r'^(?P<api>(old|stable))/(?P<filter_name>(tag|language|license|author))/'
     '(?P<filter_value>(.*))/$', 'weechat.plugins.views.scripts'),
    (r'^(?P<api>(old|stable))/sort/(?P<sort_key>(name|language|license|'
     'min_weechat|max_weechat|author|added|updated))/$',
     'weechat.plugins.views.scripts'),
    (r'^source/(?P<scriptid>\d+)/$', 'weechat.plugins.views.script_source'),
    (r'^source/(?P<api>(old|stable))/(?P<scriptname>[a-zA-Z0-9_.]+)\.html/$',
     'weechat.plugins.views.script_source'),
    (r'^source/(?P<api>(old|stable))/(?P<scriptname>[a-zA-Z0-9_.]+)/$',
     'weechat.plugins.views.script_source'),
    (r'^source/(?P<scriptname>[a-zA-Z0-9_.]+)\.html/$',
     'weechat.plugins.views.script_source', {'api': 'stable'}),
    (r'^source/(?P<scriptname>[a-zA-Z0-9_.]+)/$',
     'weechat.plugins.views.script_source', {'api': 'stable'}),
    (r'^add/$', 'weechat.plugins.views.form_add'),
    (r'^update/$', 'weechat.plugins.views.form_update'),
    (r'^pending/$', 'weechat.plugins.views.pending'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    (r'^addok/$',
     TemplateView.as_view(template_name='plugins/add_ok.html')),
    (r'^adderror/$',
     TemplateView.as_view(template_name='plugins/add_error.html')),
    (r'^updateok/$',
     TemplateView.as_view(template_name='plugins/update_ok.html')),
    (r'^updateerror/$',
     TemplateView.as_view(template_name='plugins/update_error.html')),
)
