# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

RUFF_VERSION ?= latest
TY_VERSION ?= latest

all: check

check: gettext lint

lint: ruff ty

gettext:
	poexam check --file-stats --rule-stats

ruff:
	uvx ruff@$(RUFF_VERSION) check

ty:
	uvx ty@$(TY_VERSION) check
