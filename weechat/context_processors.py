#
# Copyright (C) 2003-2024 Sébastien Helleu <flashcode@flashtux.org>
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

"""Context processors."""

from django.conf import settings

from weechat.common.models import Project


def theme(request):
    """Add theme variables in context."""
    user_theme = request.GET.get(
        'theme',
        request.COOKIES.get('theme', settings.THEMES[0]),
    )
    if user_theme not in settings.THEMES:
        user_theme = settings.THEMES[0]
    other_themes = [name for name in settings.THEMES if name != user_theme]
    return {
        'theme': user_theme,
        'other_themes': other_themes,
    }


def project_list(request):
    """Add project_list variable in context."""
    return {
        'project_list': Project.objects.filter(visible=1).order_by('priority'),
    }
