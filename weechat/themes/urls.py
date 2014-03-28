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

# URLs for menu ""themes"

from django.conf.urls import *
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    (r'^$', 'weechat.themes.views.themes'),
    (r'^(?P<filter_name>(author))/(?P<filter_value>(.*))/$',
     'weechat.themes.views.themes'),
    (r'^sort/(?P<sort_key>(name|version|added|updated))/$',
     'weechat.themes.views.themes'),
    (r'^source/(?P<themeid>\d+)/$', 'weechat.themes.views.theme_source'),
    (r'^source/(?P<themename>[a-zA-Z0-9_]+\.theme)\.html/$',
     'weechat.themes.views.theme_source'),
    (r'^add/$', 'weechat.themes.views.form_add'),
    (r'^update/$', 'weechat.themes.views.form_update'),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    (r'^addok/$',
     TemplateView.as_view(template_name='themes/add_ok.html')),
    (r'^adderror/$',
     TemplateView.as_view(template_name='themes/add_error.html')),
    (r'^updateok/$',
     TemplateView.as_view(template_name='themes/update_ok.html')),
    (r'^updateerror/$',
     TemplateView.as_view(template_name='themes/update_error.html')),
)
