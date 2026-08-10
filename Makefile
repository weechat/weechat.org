# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

all: check

check: gettext lint

lint: ruff ty

gettext:
	poexam check --file-stats --rule-stats

ruff:
	uvx ruff check

ty:
	uvx ty check
