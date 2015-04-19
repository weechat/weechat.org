# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2015 Sébastien Helleu <flashcode@flashtux.org>
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

"""URLs for weechat.org."""

# pylint: disable=invalid-name, no-value-for-parameter

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.views.generic.base import RedirectView

from weechat.common.views import TextTemplateView
from weechat.news.feeds import LatestNewsFeed, UpcomingEventsFeed

# admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # admin
    url(r'^%s/doc/' % settings.ADMIN_PAGE,
        include('django.contrib.admindocs.urls')),
    url(r'^%s/' % settings.ADMIN_PAGE, include(admin.site.urls)),

    # set language
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # main WeeChat URLs
    url(r'^$', 'weechat.news.views.home', {'max_info': 8, 'max_event': 4},
        name='home'),
    url(r'^news/$', 'weechat.news.views.news', name='home_news'),
    url(r'^news/(?P<info_id>\d+)/$', 'weechat.news.views.news',
        name='home_info_id'),
    url(r'^news/(?P<info_id>\d+)/(.*)/$', 'weechat.news.views.news',
        name='home_info_id_title'),
    url(r'^events/$', 'weechat.news.views.events', name='home_events'),
    url(r'^events/(?P<event_id>\d+)/$', 'weechat.news.views.events',
        name='home_event_id'),
    url(r'^events/(?P<event_id>\d+)/(.*)/$', 'weechat.news.views.events',
        name='home_event_id_title'),
    url(r'^about/', include('weechat.about.urls')),
    url(r'^doc/', include('weechat.doc.urls')),
    url(r'^faq/$', RedirectView.as_view(url='/files/doc/weechat_faq.en.html'),
        name='faq'),
    url(r'^download/', include('weechat.download.urls')),
    url(r'^scripts/', include('weechat.plugins.urls')),
    url(r'^themes/', include('weechat.themes.urls')),
    url(r'^dev/', include('weechat.dev.urls')),

    # old URLs (redirected to new pages)
    url(r'^features/$', RedirectView.as_view(url='/about/features/')),
    url(r'^screenshots/$', RedirectView.as_view(url='/about/screenshots/')),
    url(r'^story/$', RedirectView.as_view(url='/about/history/')),
    url(r'^donate/$', RedirectView.as_view(url='/about/donate/')),
    url(r'^security/$', RedirectView.as_view(url='/download/security/')),
    url(r'^stats/$', RedirectView.as_view(url='/dev/stats/')),
    url(r'^info/$', RedirectView.as_view(url='/dev/info/')),
    url(r'^info/(?P<name>[a-zA-Z0-9-_]*)/$', 'weechat.dev.views.info'),
    url(r'^support/$', RedirectView.as_view(url='/dev/support/')),

    # feeds
    url(r'^feeds/news/$', LatestNewsFeed(), name='feeds_news'),
    url(r'^feeds/events/$', UpcomingEventsFeed(), name='feeds_events'),

    # files and media
    url('^files$', RedirectView.as_view(url='/files/')),
    url('^media$', RedirectView.as_view(url='/media/')),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    url(r'^robots\.txt$',
        TextTemplateView.as_view(template_name='robots.txt')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        # static files
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^files/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.FILES_ROOT}),
    )
