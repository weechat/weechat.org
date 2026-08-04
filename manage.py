#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weechat.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
