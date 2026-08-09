# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Common models."""

from django.db import models


class Project(models.Model):
    """A project."""
    id = models.AutoField(primary_key=True)
    visible = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        hidden = '' if self.visible else ', hidden'
        return f'{self.name} ({self.priority}){hidden}'

    class Meta:
        ordering = ('priority',)
