# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Common classes/functions for admin."""

from collections.abc import Mapping
from typing import Any, ClassVar

from django.contrib import admin
from django.db import models
from django.forms import TextInput


class WeechatAdmin(admin.ModelAdmin):
    """WeeChat admin."""
    list_per_page = 1000
    formfield_overrides: ClassVar[
        'Mapping[type[models.Field[Any, Any]], Mapping[str, Any]]'
    ] = {
        models.CharField: {'widget': TextInput(attrs={'size': '75'})},
    }
