# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for Debian repositories."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.debian.models import Builder, Repo, Version

admin.site.register(Version, WeechatAdmin)
admin.site.register(Builder, WeechatAdmin)
admin.site.register(Repo, WeechatAdmin)
