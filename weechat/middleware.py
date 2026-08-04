# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Middlewares."""

from django.conf import settings

COOKIE_AGE = 3600 * 24 * 365


class ThemeMiddleware:
    """Theme middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def set_cookie(cls, response, theme):
        """Set the theme cookie."""
        if theme not in settings.THEMES:
            theme = settings.THEMES[0]
        response.set_cookie('theme', value=theme, max_age=COOKIE_AGE)

    def __call__(self, request):
        response = self.get_response(request)
        if 'theme' in request.GET:
            self.set_cookie(response, request.GET['theme'])
        if 'theme' in request.COOKIES \
                and request.COOKIES['theme'] not in settings.THEMES:
            self.set_cookie(response, settings.THEMES[0])
        return response
