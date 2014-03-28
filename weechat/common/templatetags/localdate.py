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

from datetime import datetime

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils import dateformat
from django.utils.translation import ugettext

register = template.Library()


@register.filter()
def localdate(value):
    """Format date with localized date format."""
    try:
        format = ugettext(settings.DATE_FORMAT)
        return dateformat.format(value, format)
    except:
        return ''


@register.filter()
def localstrdate(value):
    """Format string date with localized date format."""
    try:
        format = ugettext(settings.DATE_FORMAT)
        dt = datetime.strptime(value, '%Y-%m-%d')
        return dateformat.format(dt, format)
    except:
        return ''
