# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""URLs for "doc" menu."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from weechat.doc.views import (
    documentation as view_doc,
)
from weechat.doc.views import (
    documentation_link as view_doc_link,
)
from weechat.doc.views import (
    security_all as view_security,
)
from weechat.doc.views import (
    security_version as view_security_version,
)
from weechat.doc.views import (
    security_wsa as view_security_wsa,
)

LEGACY_DOC = 'faq|user|plugin_api|scripting|quickstart|dev|relay_api|relay_weechat'

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
    # /doc/security
    re_path(r'^security/(?P<wsa>WSA-[0-9]{4}-[0-9]+)/$',
            view_security_wsa, name='doc_project_security_wsa'),
    re_path(r'security/version/$', view_security_version,
            name='doc_project_security_versions'),
    re_path(r'security/version/(?P<version>[0-9.]+)/$',
            view_security_version, name='doc_project_security_version'),

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
