#
# Copyright (C) 2003-2021 Sébastien Helleu <flashcode@flashtux.org>
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

"""Some useful tracker functions."""

import re

from django.conf import settings

GITHUB_LINK = 'https://github.com/weechat/weechat/issues/%s'
GITHUB_PATTERN = re.compile(r'(issue|close|closes|closed|fix|fixes|fixed|'
                            'resolve|resolves|resolved) #([0-9]+)')

SAVANNAH_LINKS = {
    'bug': 'https://savannah.nongnu.org/bugs/?%s',
    'task': 'https://savannah.nongnu.org/task/?%s',
    'patch': 'https://savannah.nongnu.org/patch/?%s',
}
SAVANNAH_PATTERN = re.compile(r'(bug|task|patch) #([0-9]+)')


def _replace_github_link(match):
    """Replace a match of GitHub keyword (like "closes #123") by URL."""
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (
        GITHUB_LINK % match.group(2),
        match.group(0))


def _replace_savannah_link(match):
    """Replace a match of Savannah keyword (like "bug #12345") by URL."""
    if match.group(1) not in SAVANNAH_LINKS:
        return match.group(0)
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (
        SAVANNAH_LINKS[match.group(1)] % match.group(2),
        match.group(0))


def _replace_link(tracker):
    """Replace GitHub and Savannah links in a string."""
    string = GITHUB_PATTERN.sub(_replace_github_link, tracker)
    return SAVANNAH_PATTERN.sub(_replace_savannah_link, string)


def tracker_links(tracker):
    """Replace tracker items by URLs.

    Replace GitHub tracker item(s) (for example: "closes #123")
    and savannah tracker item(s) (for example: "bug #12345")
    by URL(s) to this/these item(s).
    """
    if not tracker:
        return ''
    items = [_replace_link(item) for item in tracker.split(',')]
    return '<br>'.join(items)


def split_commit(commit):
    """
    Return repository and commit id with a commit name, with one of these
    formats:

        org/repo@commit
        repo@commit
        commit

    Default repository is weechat/weechat.
    """
    if '@' not in commit:
        return ('weechat/weechat', commit)
    repo, commit_id = commit.split('@', 1)
    if '/' not in repo:
        repo = f'weechat/{repo}'
    return (repo, commit_id)


def commits_links(commits):
    """Replace commits or branches by GitHub URLs."""
    if not commits:
        return ''
    images = []
    for commit in commits.split(','):
        objtype = 'commit'
        img = 'link.png'
        title = ''
        if commit.startswith('commit/'):
            commit = commit[7:]
        if commit.startswith('tree/'):
            objtype = 'tree'
            commit = commit[5:]
            img = 'link_twin.png'
            title = f' title="branch: {commit}"'
        repo, commit_id = split_commit(commit)
        images.append(f'<a href="https://github.com/{repo}/{objtype}/'
                      f'{commit_id}" target="_blank" rel="noopener">'
                      f'<img src="{settings.MEDIA_URL}images/{img}" '
                      f'width="16" height="16" alt="*"{title}></a>')
    return ' '.join(images)


def spec_link(url_spec):
    """Replace specification id by URLs to specification."""
    if not url_spec:
        return ''
    return (f'<a href="{url_spec}" '
            f'target="_blank" rel="noopener">'
            f'<img src="{settings.MEDIA_URL}images/link.png" '
            f'width="16" height="16" alt="*"></a>')
