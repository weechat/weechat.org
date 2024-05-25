#
# Copyright (C) 2003-2024 Sébastien Helleu <flashcode@flashtux.org>
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
from django.views.generic.base import RedirectView

from weechat.doc.views import (
    documentation as view_doc,
    documentation_link as view_doc_link,
    security_all as view_security,
    security_wsa as view_security_wsa,
    security_version as view_security_version,
)

LEGACY_DOC = 'faq|user|plugin_api|scripting|quickstart|dev|relay_protocol'

urlpatterns = [
    path('', view_doc, name='doc'),

    # legacy URLs (redirected to new pages)
    path('stable/', RedirectView.as_view(url='/doc/weechat/stable/')),
    path('devel/', RedirectView.as_view(url='/doc/weechat/devel/')),
    path('security/', RedirectView.as_view(url='/doc/weechat/security/')),

    # docs per project/version
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/$', view_doc, name='doc_project_version'),
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/(?P<version>stable|devel)/$',
            view_doc, name='doc_project_version'),
    re_path(r'(?P<project>[a-zA-Z0-9._-]+)/security/$', view_security,
            name='doc_project_security'),
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/security/(?P<wsa>WSA-[0-9]{4}-[0-9]+)/$',
            view_security_wsa, name='doc_project_security_wsa'),
    re_path(r'(?P<project>[a-zA-Z0-9._-]+)/security/version/$', view_security_version,
            name='doc_project_security_versions'),
    re_path(r'(?P<project>[a-zA-Z0-9._-]+)/security/version/(?P<version>[0-9.]+)/$',
            view_security_version, name='doc_project_security_version'),

    # legacy shortcuts: project missing, weechat is default
    # /doc/stable/user
    re_path(rf'^(?P<version>stable|devel)/(?P<name>{LEGACY_DOC})/$', view_doc_link),
    # /doc/user
    re_path(rf'^(?P<name>{LEGACY_DOC})/$', view_doc_link),
    # /doc/stable/user/en
    re_path(rf'^(?P<version>stable|devel)/(?P<name>{LEGACY_DOC})/'
            r'(?P<lang>[a-z][a-z])/$',
            view_doc_link),
    # /doc/user/en
    re_path(rf'^(?P<name>{LEGACY_DOC})/(?P<lang>[a-z][a-z])/$', view_doc_link),

    # shortcuts
    # /doc/weechat/stable/user
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/(?P<version>stable|devel)/'
            r'(?P<name>[a-z_]+)/$', view_doc_link),
    # /doc/weechat/user
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/(?P<name>[a-z_]+)/$', view_doc_link),
    # /doc/weechat/stable/user/en
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/(?P<version>stable|devel)/'
            r'(?P<name>[a-z_]+)/(?P<lang>[a-z][a-z])/$',
            view_doc_link),
    # /doc/weechat/user/fr
    re_path(r'^(?P<project>[a-zA-Z0-9._-]+)/(?P<name>[a-z_]+)/'
            r'(?P<lang>[a-z][a-z])/$', view_doc_link),
]
