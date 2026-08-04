# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Some useful path functions."""

import os

from django.conf import settings


def __path_join(base, *args):
    """
    Join multiple paths after 'base' and ensure the result is still
    under 'base'.
    """
    base = os.path.normpath(base)
    directory = os.path.normpath(os.path.join(base, *args))
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
