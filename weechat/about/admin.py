#
# Copyright (C) 2003-2020 Sébastien Helleu <flashcode@flashtux.org>
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

"""Admin for "about" menu."""

from django.contrib import admin

from weechat.common.admin import WeechatAdmin
from weechat.about.models import Screenshot, Keydate, Sponsor

admin.site.register(Screenshot, WeechatAdmin)
admin.site.register(Keydate, WeechatAdmin)
admin.site.register(Sponsor, WeechatAdmin)
