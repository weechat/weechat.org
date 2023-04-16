#
# Copyright (C) 2003-2023 Sébastien Helleu <flashcode@flashtux.org>
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

"""Some useful tags for localized dates."""

from django import template
from django.conf import settings
from django.utils import dateformat
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

# pylint: disable=invalid-name
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
    if fmt == 'date':
        fmt = gettext(settings.DATE_FORMAT)
    elif fmt == 'datetime':
        fmt = gettext(settings.DATETIME_FORMAT)
    date_iso = value.isoformat()
    date_fmt = dateformat.format(value, fmt)
    return mark_safe(f'<time datetime="{date_iso}">{date_fmt}</time>')
