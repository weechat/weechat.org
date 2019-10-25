# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2019 Sébastien Helleu <flashcode@flashtux.org>
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

"""Views for "about" menu."""

import os

from django import __version__ as django_version
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import render
from django.utils.translation import ugettext
from sys import version as python_version

from weechat.about.models import (
    Screenshot,
    Keydate,
    Sponsor,
    SPONSOR_TYPE_CHOICES,
    SPONSOR_TYPE_SVG,
)
from weechat.common.path import media_path_join
from weechat.download.models import Release


def screenshots(request, app='weechat', filename=''):
    """
    Page with one screenshot (if filename given),
    or all screenshots as thumbnails.
    """
    if filename:
        try:
            screenshot = Screenshot.objects.get(app=app, filename=filename)
        except ObjectDoesNotExist:
            screenshot = None
        return render(
            request,
            'about/screenshots.html',
            {
                'app': app,
                'filename': filename,
                'screenshot': screenshot,
            },
        )
    else:
        screenshot_list = (Screenshot.objects.filter(app=app)
                           .order_by('priority'))
        return render(
            request,
            'about/screenshots.html',
            {
                'app': app,
                'screenshot_list': screenshot_list,
            },
        )


def history(request):
    """Page with WeeChat history, including key dates."""
    release_list = (Release.objects.all().exclude(version='devel')
                    .order_by('-date'))
    releases = []
    for release in release_list:
        name = 'weechat-%s.png' % release.version
        if os.path.exists(media_path_join('images', 'story', name)):
            releases.append((release.version, release.date))
    return render(
        request,
        'about/history.html',
        {
            'releases': releases,
            'keydate_list': Keydate.objects.all().order_by('date'),
        },
    )


def about(request, extra_info=False):
    """About WeeChat.org."""
    context = {}
    if extra_info:
        context.update({
            'extra_info': {
                'django': django_version,
                'python': python_version,
            },
        })
    return render(request, 'about/weechat.org.html', context)


def donate(request, sort_key='date', view_key=''):
    """Page with link for donation and list of sponsors."""
    sort_key_top = 'top10'
    sort_key_top_count = 10
    sort_count = 0
    if sort_key.startswith('top'):
        sort_key_top = sort_key
        sort_count = max(int(sort_key[3:]), 1)
        sort_key_top_count = sort_count
        sort_key = 'top'

    if sort_key == 'type':
        sponsor_list = (Sponsor.objects.values('sponsortype')
                        .annotate(amount=Sum('amount'))
                        .order_by('-amount'))
        total = sum(sponsor['amount'] for sponsor in sponsor_list)
        for sponsor in sponsor_list:
            sponsor['sponsortype_i18n'] = ugettext(
                dict(SPONSOR_TYPE_CHOICES)[sponsor['sponsortype']])
            sponsor['sponsortype_svg'] = \
                SPONSOR_TYPE_SVG[sponsor['sponsortype']]
    elif sort_key == 'top':
        sponsor_list = (Sponsor.objects.values('sponsortype', 'name')
                        .annotate(amount=Sum('amount'))
                        .order_by('-amount')[:sort_count])
        total = sum(sponsor['amount'] for sponsor in sponsor_list)
        for sponsor in sponsor_list:
            sponsor['sponsortype_i18n'] = ugettext(
                dict(SPONSOR_TYPE_CHOICES)[sponsor['sponsortype']])
            sponsor['sponsortype_svg'] = \
                SPONSOR_TYPE_SVG[sponsor['sponsortype']]
    else:
        # by default: sort by date
        sponsor_list = Sponsor.objects.all().order_by('-date', '-id')
        total = sum(sponsor.amount for sponsor in sponsor_list)

    view_amount = False
    try:
        if view_key and view_key == settings.KEY_VIEWAMOUNT:
            view_amount = True
    except AttributeError:
        pass

    return render(
        request,
        'donate.html',
        {
            'sponsor_list': sponsor_list,
            'sort_key': sort_key,
            'sort_count': sort_count,
            'sort_key_top': sort_key_top,
            'sort_key_top_count': sort_key_top_count,
            'view_amount': view_amount,
            'total': total,
        },
    )
