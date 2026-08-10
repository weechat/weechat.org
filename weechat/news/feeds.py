# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""WeeChat feeds."""

import datetime

from django.contrib.syndication.views import Feed

from weechat.news.models import Info


class WeechatFeed(Feed):
    """A WeeChat feed."""

    def get_object(self, request, *args, **kwargs):
        self.request = request

    def item_link(self, item):
        """Return link to item by using the domain sent in the request."""
        return (f'{self.request.scheme}://{self.request.get_host()}/news/'
                f'{item.id}')

    def item_pubdate(self, info):
        """Return idem date."""
        return info.date


class LatestNewsFeed(WeechatFeed):
    """Feed with latest news."""
    title = 'WeeChat news'
    description = title
    link = '/news/'

    def items(self):
        """Return items with date in the past."""
        return (Info.objects.filter(visible=1)
                .filter(date__lte=datetime.datetime.now(tz=datetime.UTC)).order_by('-date')[:10])


class UpcomingEventsFeed(WeechatFeed):
    """Feed with upcoming events."""
    title = 'Upcoming WeeChat events'
    description = title
    link = '/events/'

    def items(self):
        """Return items with date in the future."""
        return (Info.objects.filter(visible=1)
                .filter(date__gt=datetime.datetime.now(tz=datetime.UTC)).order_by('date')[:10])
