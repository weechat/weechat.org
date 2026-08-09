# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Models for "dev" menu."""

from datetime import date

from django.db import models
from django.utils.html import format_html

from weechat.common.tracker import commits_links, tracker_links
from weechat.common.templatetags.localdate import localdate
from weechat.download.models import Release


class Task(models.Model):
    """A task (a new feature or bug to fix)."""
    id = models.AutoField(primary_key=True)
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
                return format_html('≈ {}', localdate(self.version.date))
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
