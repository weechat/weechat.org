# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Some useful functions for versions."""

import re

from django import template

register = template.Library()


@register.filter()
def version_as_int(version):
    """
    Return a string with number of version, for example: 0.4.1 gives:
    262400 (0x00040100).
    """
    try:
        items = version.split('.', 3)
        value = [0, 0, 0, 0]
        for i in range(4):
            if i < len(items):
                value[i] = int(re.sub('[^0-9].*', '', items[i]))
                if value[i] < 0:
                    value[i] = 0
                elif value[i] > 0xFF:
                    value[i] = 0xFF
        return (value[0] << 24) | (value[1] << 16) | (value[2] << 8) | value[3]
    except:  # noqa: E722
        return 0
