#
# Copyright (C) 2003-2021 Sébastien Helleu <flashcode@flashtux.org>
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

"""URLs for weechat.org."""

# pylint: disable=invalid-name

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from weechat.common.views import TextTemplateView
from weechat.dev.views import info as view_info
from weechat.news.feeds import LatestNewsFeed, UpcomingEventsFeed
from weechat.news.views import (
    home as view_home,
    news as view_news,
    events as view_events,
)
from weechat.about.views import donate as view_donate

# admin
admin.autodiscover()

urlpatterns = [
    # favicon.ico
    url(r'^favicon.ico$',
        RedirectView.as_view(url=f'{settings.MEDIA_URL}images/favicon.png',
                             permanent=True)),

    # admin
    url(rf'^{settings.ADMIN_PAGE}/doc/',
        include('django.contrib.admindocs.urls')),
    url(rf'^{settings.ADMIN_PAGE}/', admin.site.urls),

    # set language
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # legacy URLs (redirected to new pages)
    url(r'^features/$', RedirectView.as_view(url='/about/features/')),
    url(r'^screenshots/$', RedirectView.as_view(url='/about/screenshots/')),
    url(r'^story/$', RedirectView.as_view(url='/about/history/')),
    url(r'^about/donate/$', RedirectView.as_view(url='/donate/')),
    url(r'^security/$', RedirectView.as_view(url='/doc/security/')),
    url(r'^download/security/$', RedirectView.as_view(url='/doc/security/')),
    url(r'^stats/$', RedirectView.as_view(url='/dev/stats/')),
    url(r'^info/$', RedirectView.as_view(url='/dev/info/')),
    url(r'^info/(?P<name>[a-zA-Z0-9-_]*)/$', view_info),
    url(r'^support/$', RedirectView.as_view(url='/about/support/')),
    url(r'^dev/support/$', RedirectView.as_view(url='/about/support/')),

    # main WeeChat URLs
    url(r'^$', view_home, {'max_info': 4, 'max_event': 4},
        name='home'),
    url(r'^news/$', view_news, name='home_news'),
    url(r'^news/(?P<info_id>\d+)/$', view_news, name='home_info_id'),
    url(r'^news/(?P<info_id>\d+)/(.*)/$', view_news,
        name='home_info_id_title'),
    url(r'^events/$', view_events, name='home_events'),
    url(r'^donate/$', view_donate, name='donate'),
    url(r'^donate/sort/(?P<sort_key>(date|type|top[0-9]+))/$', view_donate,
        name='donate_sort'),
    url(r'^donate/sort/(?P<sort_key>(date|type|top[0-9]+))/'
        r'view/(?P<view_key>[a-zA-Z0-9_]*)/$',
        view_donate),
    url(r'^about/', include('weechat.about.urls')),
    url(r'^doc/', include('weechat.doc.urls')),
    url(r'^faq/$', RedirectView.as_view(url='/files/doc/weechat_faq.en.html'),
        name='faq'),
    url(r'^download/', include('weechat.download.urls')),
    url(r'^scripts/', include('weechat.scripts.urls')),
    url(r'^themes/', include('weechat.themes.urls')),
    url(r'^dev/', include('weechat.dev.urls')),

    # feeds
    url(r'^feeds/news/$', LatestNewsFeed(), name='feeds_news'),
    url(r'^feeds/events/$', UpcomingEventsFeed(), name='feeds_events'),

    # files and media
    url('^files$', RedirectView.as_view(url='/files/')),
    url('^media$', RedirectView.as_view(url='/media/')),

    # robots.txt
    url(r'^robots\.txt$',
        TextTemplateView.as_view(template_name='robots.txt')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.FILES_URL,
                          document_root=settings.FILES_ROOT)
