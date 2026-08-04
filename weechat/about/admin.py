# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for "about" menu."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.about.models import Screenshot, Keydate, Sponsor

admin.site.register(Screenshot, WeechatAdmin)
admin.site.register(Keydate, WeechatAdmin)
admin.site.register(Sponsor, WeechatAdmin)
