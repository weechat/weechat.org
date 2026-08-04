# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for news."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.news.models import Info

admin.site.register(Info, WeechatAdmin)
