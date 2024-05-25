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

"""Common models."""

from django.db import models


class Project(models.Model):
    """A project."""
    visible = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        hidden = '' if self.visible else ', hidden'
        return f'{self.name} ({self.priority}){hidden}'

    class Meta:
        ordering = ['priority']
