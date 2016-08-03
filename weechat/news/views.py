# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2016 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for news."""

from datetime import datetime

from django.shortcuts import render
from django.template import RequestContext

from weechat.download.models import Release
from weechat.news.models import Info


def render_homepage(request, info_list, max_info, event_list, max_event):
    """Render homepage."""
    return render(
        request,
        'home/home.html',
        {
            'release_stable': Release.objects.get(version='stable'),
            'info_list': info_list,
            'max_info': max_info,
            'event_list': event_list,
            'max_event': max_event,
        },
    )


def home(request, max_info=None, max_event=None):
    """Homepage."""
    now = datetime.now()
    info_list = Info.objects.all().filter(visible=1).filter(date__lte=now) \
        .order_by('-date')
    if max_info:
        info_list = info_list[:max_info]
    event_list = Info.objects.all().filter(visible=1).filter(date__gt=now) \
        .order_by('date')
    if max_event:
        event_list = event_list[:max_event]
    return render_homepage(request, info_list, max_info, event_list, max_event)


def news(request, info_id=None):
    """Homepage with only news."""
    try:
        if info_id:
            info_list = [Info.objects.get(id=info_id, visible=1)]
        else:
            info_list = Info.objects.all().filter(visible=1) \
                .filter(date__lte=datetime.now()).order_by('-date')
    except:
        info_list = None
    return render_homepage(request, info_list, None, None, None)


def events(request, event_id=None):
    """Homepage with only upcoming events."""
    try:
        if event_id:
            event_list = [Info.objects.get(id=event_id, visible=1)]
        else:
            event_list = Info.objects.all().filter(visible=1) \
                .filter(date__gt=datetime.now()).order_by('date')
    except:
        event_list = None
    return render_homepage(request, None, None, event_list, None)
