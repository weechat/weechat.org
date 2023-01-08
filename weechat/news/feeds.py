#
# Copyright (C) 2003-2023 Sébastien Helleu <flashcode@flashtux.org>
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

"""WeeChat feeds."""

from datetime import datetime

from django.contrib.syndication.views import Feed

from weechat.news.models import Info


class WeechatFeed(Feed):
    """A WeeChat feed."""

    def get_object(self, request, *args, **kwargs):
        # pylint: disable=attribute-defined-outside-init
        self.request = request

    def item_link(self, item):
        """Return link to item by using the domain sent in the request."""
        return (f'{self.request.scheme}://{self.request.get_host()}/news/'
                f'{item.id}')

    def item_pubdate(self, info):
        """Return idem date."""
        # pylint: disable=all
        return info.date


class LatestNewsFeed(WeechatFeed):
    """Feed with latest news."""
    title = 'WeeChat news'
    description = title
    link = '/news/'

    def items(self):
        """Return items with date in the past."""
        # pylint: disable=all
        return (Info.objects.filter(visible=1)
                .filter(date__lte=datetime.now()).order_by('-date')[:10])


class UpcomingEventsFeed(WeechatFeed):
    """Feed with upcoming events."""
    title = 'Upcoming WeeChat events'
    description = title
    link = '/events/'

    def items(self):
        """Return items with date in the future."""
        # pylint: disable=all
        return (Info.objects.filter(visible=1)
                .filter(date__gt=datetime.now()).order_by('date')[:10])
