# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Some useful tags for localized dates."""

import datetime

from django import template
from django.conf import settings
from django.utils import dateformat, timezone
from django.utils.html import format_html
from django.utils.translation import gettext

register = template.Library()


@register.filter()
def localdate(value, fmt='date'):
    """
    Format date with localized date/time format.
    If fmt == "date", the localized date format is used.
    If fmt == "datetime", the localized date/fime format is used.
    Another fmt it is used as-is.
    """
    if not value:
        return ''
    if isinstance(value, datetime.datetime) and timezone.is_aware(value):
        value = timezone.localtime(value)
    if fmt == 'date':
        fmt = gettext(settings.DATE_FORMAT)
    elif fmt == 'datetime':
        fmt = gettext(settings.DATETIME_FORMAT)
    date_iso = value.isoformat()
    date_fmt = dateformat.format(value, fmt)
    return format_html('<time datetime="{}">{}</time>', date_iso, date_fmt)
