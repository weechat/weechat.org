#
# Copyright (C) 2003-2022 Sébastien Helleu <flashcode@flashtux.org>
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
