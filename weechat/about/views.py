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

from os import path

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render_to_response
from django.template import RequestContext

from weechat.about.models import Screenshot, Keydate, Sponsor
from weechat.common.path import media_path_join
from weechat.download.models import Release


def screenshots(request, filename=''):
    """
    Page with one screenshot (if filename given),
    or all screenshots as thumbnails.
    """
    if filename:
        try:
            screenshot = Screenshot.objects.get(filename=filename)
        except:
            screenshot = None
        return render_to_response(
            'about/screenshots.html',
            {
                'filename': filename,
                'screenshot': screenshot,
            },
            context_instance=RequestContext(request))
    else:
        screenshots = Screenshot.objects.all().order_by('priority')
        return render_to_response('about/screenshots.html',
                                  {'screenshots': screenshots},
                                  context_instance=RequestContext(request))


def history(request):
    """Page with WeeChat history, including key dates."""
    release_list = \
        Release.objects.all().exclude(version='devel').order_by('-date')
    releases = []
    for release in release_list:
        name = 'weechat-%s.png' % release.version
        if path.exists(media_path_join('images', 'story', name)):
            releases.append((release.version, release.date))
    return render_to_response(
        'about/history.html',
        {
            'releases': releases,
            'keydate_list': Keydate.objects.all().order_by('date'),
        },
        context_instance=RequestContext(request))


def donate(request, sort_key='date', view_key=''):
    """Page with link for donation and list of sponsors."""
    if sort_key == 'top10':
        sponsor_list = Sponsor.objects.values('name').\
            annotate(amount=Sum('amount')).order_by('-amount')[:10]
        total = sum(sponsor['amount'] for sponsor in sponsor_list)
    else:
        # by default: sort by date
        sponsor_list = Sponsor.objects.all().order_by('-date', '-id')
        total = sum(sponsor.amount for sponsor in sponsor_list)
    view_amount = False
    try:
        if view_key and view_key == settings.KEY_VIEWAMOUNT:
            view_amount = True
    except:
        pass
    return render_to_response(
        'about/donate.html',
        {
            'sponsor_list': sponsor_list,
            'sort_key': sort_key,
            'view_amount': view_amount,
            'total': total,
        },
        context_instance=RequestContext(request))
