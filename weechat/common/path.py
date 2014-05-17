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

"""Some useful path functions."""

from os import path

from django.conf import settings


def __path_join(base, *args):
    """
    Join multiple paths after 'base' and ensure the result is still
    under 'base'.
    """
    base = path.normpath(base)
    directory = path.normpath(path.join(base, *args))
    if directory.startswith(base):
        return directory
    return ''


def project_path_join(*args):
    """Join multiple paths after settings.BASE_DIR."""
    return __path_join(settings.BASE_DIR, *args)


def files_path_join(*args):
    """Join multiple paths after settings.FILES_ROOT."""
    return __path_join(settings.FILES_ROOT, *args)


def media_path_join(*args):
    """Join multiple paths after settings.MEDIA_ROOT."""
    return __path_join(settings.MEDIA_ROOT, *args)


def repo_path_join(*args):
    """Join multiple paths after settings.REPO_DIR."""
    return __path_join(settings.REPO_DIR, *args)
