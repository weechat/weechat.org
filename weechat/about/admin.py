# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for "about" menu."""

from django.contrib import admin

from weechat.about.models import Keydate, Screenshot, Sponsor
from weechat.common.admin import WeechatAdmin

admin.site.register(Screenshot, WeechatAdmin)
admin.site.register(Keydate, WeechatAdmin)
admin.site.register(Sponsor, WeechatAdmin)
