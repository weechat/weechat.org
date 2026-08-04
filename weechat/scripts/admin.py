# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for "scripts" menu."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.scripts.models import Script

admin.site.register(Script, WeechatAdmin)
