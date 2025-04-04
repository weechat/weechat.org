#
# SPDX-FileCopyrightText: 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

"""Tag to obfuscate e-mails in HTML code."""

from django import template
from django.utils.safestring import mark_safe

# pylint: disable=invalid-name
register = template.Library()


@register.filter()
def txt2html(value):
    """Return text with html ascii codes (for example anti-spam for emails)."""
    return mark_safe(''.join([f'&#{ord(c)};' for c in value]))


register.simple_tag(txt2html)
