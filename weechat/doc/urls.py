#
# Copyright (C) 2003-2022 Sébastien Helleu <flashcode@flashtux.org>
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

"""URLs for "doc" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path

from weechat.doc.views import (
    documentation as view_doc,
    documentation_link as view_doc_link,
    security_all as view_security,
    security_wsa as view_security_wsa,
    security_version as view_security_version,
)

urlpatterns = [
    path('', view_doc, name='doc'),
    re_path(r'^(?P<version>stable|devel|old)/$', view_doc, name='doc_version'),
    path('security/', view_security, name='doc_security'),
    re_path(r'^security/(?P<wsa>WSA-[0-9]{4}-[0-9]+)/$', view_security_wsa,
            name='doc_security_wsa'),
    path('security/version/', view_security_version,
         name='doc_security_versions'),
    re_path('security/version/(?P<version>[0-9.]+)/$', view_security_version,
            name='doc_security_version'),

    # shortcuts
    re_path(r'^(?P<version>stable|devel)/(?P<name>[a-z_]+)/$', view_doc_link),
    re_path(r'^(?P<name>[a-z_]+)/$', view_doc_link),
    re_path(r'^(?P<version>stable|devel)/(?P<name>[a-z_]+)/'
            r'(?P<lang>[a-z_]+)/$',
            view_doc_link),
    re_path(r'^(?P<name>[a-z_]+)/(?P<lang>[a-z_]+)/$', view_doc_link),
]
