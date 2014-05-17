# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2014 Sébastien Helleu <flashcode@flashtux.org>
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
# along with WeeChat.org.  If not, see <http://www.gnu.org/licenses/>.
#

"""Some useful functions for versions."""

import re

from django import template

# pylint: disable=invalid-name
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
        for i in range(0, 4):
            if i < len(items):
                value[i] = int(re.sub('[^0-9].*', '', items[i]))
                if value[i] < 0:
                    value[i] = 0
                elif value[i] > 0xFF:
                    value[i] = 0xFF
        return (value[0] << 24) | (value[1] << 16) | (value[2] << 8) | value[3]
    except:
        return 0
