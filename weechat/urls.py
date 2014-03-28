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

from django.conf import settings
from django.conf.urls import *
from django.views.generic.base import RedirectView

from weechat.common.views import TextTemplateView
from weechat.news.feeds import LatestNewsFeed, UpcomingEventsFeed

# admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # admin
    (r'^%s/doc/' % settings.ADMIN_PAGE,
     include('django.contrib.admindocs.urls')),
    (r'^%s/' % settings.ADMIN_PAGE, include(admin.site.urls)),

    # set language
    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^$', 'weechat.news.views.home', {'max_info': 6, 'max_event': 4}),
    (r'^news/$', 'weechat.news.views.news'),
    (r'^news/(?P<info_id>\d+)(/.*)?/$', 'weechat.news.views.news'),
    (r'^events/$', 'weechat.news.views.events'),
    (r'^events/(?P<event_id>\d+)(/.*)?/$', 'weechat.news.views.events'),
    (r'^about/', include('weechat.about.urls')),
    (r'^doc/', include('weechat.doc.urls')),
    (r'^faq/$', RedirectView.as_view(url='/files/doc/weechat_faq.en.html')),
    (r'^download/', include('weechat.download.urls')),
    (r'^plugins/', include('weechat.plugins.urls')),
    (r'^scripts/', include('weechat.plugins.urls')),
    (r'^themes/', include('weechat.themes.urls')),
    (r'^dev/', include('weechat.dev.urls')),

    # old URLs (redirected to new pages)
    (r'^features/$', RedirectView.as_view(url='/about/features/')),
    (r'^screenshots/$', RedirectView.as_view(url='/about/screenshots/')),
    (r'^story/$', RedirectView.as_view(url='/about/history/')),
    (r'^donate/$', RedirectView.as_view(url='/about/donate/')),
    (r'^security/$', RedirectView.as_view(url='/download/security/')),
    (r'^stats/$', RedirectView.as_view(url='/dev/stats/')),
    (r'^info/$', RedirectView.as_view(url='/dev/info/')),
    (r'^info/(?P<info>[a-zA-Z0-9-_]*)/$', 'weechat.dev.views.info'),
    (r'^support/$', RedirectView.as_view(url='/dev/support/')),

    # feeds
    (r'^feeds/news/$', LatestNewsFeed()),
    (r'^feeds/events/$', UpcomingEventsFeed()),

    # files and media
    ('^files$', RedirectView.as_view(url='/files/')),
    ('^media$', RedirectView.as_view(url='/media/')),
)

urlpatterns += patterns(
    'django.views.generic.simple',
    (r'^robots\.txt$', TextTemplateView.as_view(template_name='robots.txt')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        # static files
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^files/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.FILES_ROOT}),
    )
