# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
