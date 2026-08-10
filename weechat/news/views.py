# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Views for news."""

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from weechat.download.models import Release
from weechat.news.models import Info


def home(request, max_info=None, max_event=None):
    """Homepage."""
    now = datetime.datetime.now(tz=datetime.UTC)
    info_list = (Info.objects.all().filter(visible=1).filter(date__lte=now)
                 .order_by('-date'))
    if max_info:
        info_list = info_list[:max_info]
    event_list = (Info.objects.all().filter(visible=1).filter(date__gt=now)
                  .order_by('date'))
    if max_event:
        event_list = event_list[:max_event]
    try:
        stable_version = Release.objects.get(project__name='weechat',
                                             version='stable').description
        release_stable = Release.objects.get(project__name='weechat',
                                             version=stable_version)
    except ObjectDoesNotExist:
        release_stable = None
    return render(
        request,
        'home/home.html',
        {
            'release_stable': release_stable,
            'info_list': info_list,
            'event_list': event_list,
        },
    )


def paginate_news(request, info_list, pagesize):
    """Paginate list of news."""
    paginator = Paginator(info_list, pagesize)
    page = request.GET.get('page')
    try:
        infos = paginator.page(page)
    except PageNotAnInteger:
        infos = paginator.page(1)
    except EmptyPage:
        infos = paginator.page(paginator.num_pages)

    first_page = max(infos.number - 2, 1)
    last_page = min(infos.number + 2, paginator.num_pages)
    if first_page == 3:
        first_page = 1
    if last_page == paginator.num_pages - 2:
        last_page = paginator.num_pages
    smart_page_range = range(first_page, last_page + 1)

    return (infos, smart_page_range)


def render_news(request, info_list, info_id, page_name):
    """Render the paginated news."""
    pagesize = request.GET.get('pagesize', 10)
    try:
        pagesize = max(int(pagesize), 1)
    except ValueError:
        pagesize = 10
    infos, smart_page_range = paginate_news(request, info_list, pagesize)
    event = infos and infos[0].date > datetime.datetime.now(tz=datetime.UTC)
    return render(request, 'home/news.html', {
        'infos': infos,
        'info_id': info_id,
        'event': event,
        'page_name': page_name,
        'smart_page_range': smart_page_range,
        'pagesize': pagesize,
    })


def news(request, info_id=None, title=None):
    """List of news."""
    try:
        if info_id:
            info_list = [Info.objects.get(id=info_id, visible=1)]
        else:
            info_list = (Info.objects.all().filter(visible=1)
                         .filter(date__lte=datetime.datetime.now(tz=datetime.UTC)).order_by('-date'))
    except ObjectDoesNotExist:
        info_list = []
    return render_news(request, info_list, info_id, 'news')


def events(request):
    """List of upcoming events."""
    try:
        info_list = (Info.objects.all().filter(visible=1)
                     .filter(date__gt=datetime.datetime.now(tz=datetime.UTC)).order_by('date'))
    except ObjectDoesNotExist:
        info_list = []
    return render_news(request, info_list, None, 'events')
