# SPDX-FileCopyrightText: 2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tag to get value of a dict by key (variable)."""

from django import template

register = template.Library()


@register.filter()
def key_value(d, key):
    """Get value for a dict key."""
    try:
        return d[key]
    except KeyError:
        return ''
