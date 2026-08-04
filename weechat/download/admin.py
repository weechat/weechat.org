# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for "download" menu."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.download.models import Project, Release, Type, Package

admin.site.register(Project, WeechatAdmin)
admin.site.register(Release, WeechatAdmin)
admin.site.register(Type, WeechatAdmin)
admin.site.register(Package, WeechatAdmin)
