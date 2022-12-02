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

"""Models for "dev" menu."""

from datetime import date

from django.db import models
from django.utils.safestring import mark_safe

from weechat.common.tracker import commits_links, tracker_links
from weechat.common.templatetags.localdate import localdate
from weechat.download.models import Release


class Task(models.Model):
    """A task (a new feature or bug to fix)."""
    visible = models.BooleanField(default=True)
    version = models.ForeignKey(Release, on_delete=models.CASCADE)
    tracker = models.CharField(max_length=64, blank=True)
    spec = models.CharField(max_length=512, blank=True)
    status = models.IntegerField(default=0)
    commits = models.CharField(max_length=1024, blank=True)
    component = models.CharField(max_length=64, default='core')
    description = models.CharField(max_length=512)
    priority = models.IntegerField(default=0)

    def __str__(self):
        desc = (self.description
                if len(self.description) < 100
                else f'{self.description[0:100]}…')
        version = (f'({self.version.version})' if not self.visible
                   else self.version.version)
        tracker = self.tracker if self.tracker else '-'
        return (f'{version}, {tracker}, {self.status}%, {self.component}: '
                f'{desc} ({self.priority})')

    def version_date(self):
        """Return the date of version.

        It is prefixed with "≈ " if the date is in the future.
        """
        try:
            if self.version.date > date.today():
                return mark_safe(f'&asymp; {localdate(self.version.date)}')
            return localdate(self.version.date)
        except:  # noqa: E722  pylint: disable=bare-except
            return ''

    def url_tracker(self):
        """Return the tracker URL using keyword(s) in string."""
        return tracker_links(self.tracker) or '-'

    def status_remaining(self):
        """Return the remaining status as % (100 - status)."""
        return 100 - self.status

    def url_commits(self):
        """Return the URL for commit(s), as HTML."""
        return commits_links(self.commits)

    class Meta:
        ordering = ['-version__date', 'priority']
