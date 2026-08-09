# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Admin for "doc" menu."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.doc.models import Doc, Language, Security, Version

admin.site.register(Language, WeechatAdmin)
admin.site.register(Version, WeechatAdmin)
admin.site.register(Doc, WeechatAdmin)
admin.site.register(Security, WeechatAdmin)
