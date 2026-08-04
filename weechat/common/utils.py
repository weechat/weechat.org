# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Some useful functions."""


def version_to_list(version):
    """Convert version to a list of integers."""
    return list(map(int, version.split('.')))
