# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""URLs for weechat.org."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from weechat.about.views import donate as view_donate
from weechat.common.views import TextTemplateView
from weechat.dev.views import info as view_info
from weechat.doc.views import documentation_link as view_doc_link
from weechat.news.feeds import LatestNewsFeed, UpcomingEventsFeed
from weechat.news.views import (
    events as view_events,
)
from weechat.news.views import (
    home as view_home,
)
from weechat.news.views import (
    news as view_news,
)

# admin
admin.autodiscover()

urlpatterns = [
    # favicon.ico
    path('favicon.ico',
         RedirectView.as_view(url=f'{settings.MEDIA_URL}images/favicon.png',
                              permanent=True)),

    # admin
    path(f'{settings.ADMIN_PAGE}/doc/',
         include('django.contrib.admindocs.urls')),
    path(f'{settings.ADMIN_PAGE}/', admin.site.urls),

    # set language
    path('i18n/', include('django.conf.urls.i18n')),

    # legacy URLs (redirected to new pages)
    path('features/', RedirectView.as_view(url='/about/features/')),
    path('screenshots/', RedirectView.as_view(url='/about/screenshots/')),
    path('story/', RedirectView.as_view(url='/about/history/')),
    path('about/donate/', RedirectView.as_view(url='/donate/')),
    path('security/', RedirectView.as_view(url='/doc/security/')),
    path('download/security/', RedirectView.as_view(url='/doc/security/')),
    path('stats/', RedirectView.as_view(url='/dev/stats/')),
    path('info/', RedirectView.as_view(url='/dev/info/')),
    re_path(r'^info/(?P<name>[a-zA-Z0-9-_]+)/$', view_info),
    path('support/', RedirectView.as_view(url='/about/support/')),
    path('dev/support/', RedirectView.as_view(url='/about/support/')),

    # main WeeChat URLs
    path('', view_home, kwargs={'max_info': 4, 'max_event': 4}, name='home'),
    path('news/', view_news, name='home_news'),
    path('news/<int:info_id>/', view_news, name='home_info_id'),
    path('news/<int:info_id>/<str:title>/', view_news,
         name='home_info_id_title'),
    path('events/', view_events, name='home_events'),
    path('donate/', view_donate, name='donate'),
    re_path(r'^donate/sort/(?P<sort_key>(date|type|top[0-9]+))/$',
            view_donate, name='donate_sort'),
    re_path(r'^donate/sort/(?P<sort_key>(date|type|top[0-9]+))/'
            r'view/(?P<view_key>[a-zA-Z0-9_]+)/$',
            view_donate),
    path('about/', include('weechat.about.urls')),
    path('doc/', include('weechat.doc.urls')),
    path('faq/', view_doc_link, kwargs={'name': 'faq'}),
    re_path(r'^faq/(?P<lang>[a-z_]+)/$',
            view_doc_link, kwargs={'name': 'faq'}),
    path('download/', include('weechat.download.urls')),
    path('scripts/', include('weechat.scripts.urls')),
    path('themes/', include('weechat.themes.urls')),
    path('dev/', include('weechat.dev.urls')),

    # feeds
    path('feeds/news/', LatestNewsFeed(), name='feeds_news'),
    path('feeds/events/', UpcomingEventsFeed(), name='feeds_events'),

    # files and media
    path('files', RedirectView.as_view(url='/files/')),
    path('media', RedirectView.as_view(url='/media/')),

    # robots.txt
    path('robots.txt', TextTemplateView.as_view(template_name='robots.txt')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.FILES_URL,
        document_root=settings.FILES_ROOT,
        show_indexes=True,
    )
