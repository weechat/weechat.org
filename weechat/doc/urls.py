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

"""URLs for "doc" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'weechat.doc.views.documentation', name='doc'),
    url(r'^(?P<version>stable|devel|old)/$',
        'weechat.doc.views.documentation', name='doc_version'),
)
