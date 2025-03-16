#
# Copyright (C) 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
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

"""Common classes/functions for admin."""

from django.contrib import admin
from django.db import models
from django.forms import TextInput


# pylint: disable=too-many-public-methods
class WeechatAdmin(admin.ModelAdmin):
    """WeeChat admin."""
    list_per_page = 1000
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '75'})},
    }
