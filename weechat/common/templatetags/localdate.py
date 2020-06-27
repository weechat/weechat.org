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

"""Some useful tags for localized dates."""

from django import template
from django.conf import settings
from django.utils import dateformat
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext

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
    if fmt == 'date':
        fmt = ugettext(settings.DATE_FORMAT)
    elif fmt == 'datetime':
        fmt = ugettext(settings.DATETIME_FORMAT)
    return mark_safe('<time datetime="%s">%s</time>' % (
        value.isoformat(),
        dateformat.format(value, fmt),
    ))
