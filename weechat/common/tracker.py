#
# SPDX-FileCopyrightText: 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

from django.utils.safestring import mark_safe

from weechat.common.path import project_path_join


GITHUB_REPO = 'https://github.com/weechat/%(project)s'
GITHUB_LINK_ISSUE = f'{GITHUB_REPO}/issues/%(issue)s'
GITHUB_ISSUE_PATTERN = re.compile(r'(issue|close|closes|closed|fix|fixes|fixed|'
                                  'resolve|resolves|resolved) #([0-9]+)')
GITHUB_LINK_FILE = f'{GITHUB_REPO}/blob/%(ref)s/%(filename)s'
GITHUB_LINK_RELEASE = f'{GITHUB_REPO}/releases/tag/v%(version)s'


SAVANNAH_LINKS = {
    'bug': 'https://savannah.nongnu.org/bugs/?%s',
    'task': 'https://savannah.nongnu.org/task/?%s',
    'patch': 'https://savannah.nongnu.org/patch/?%s',
}
SAVANNAH_ISSUE_PATTERN = re.compile(r'(bug|task|patch) #([0-9]+)')


def _replace_github_link(match):
    """Replace a match of GitHub keyword (like "closes #123") by URL."""
    name = match.group(0)
    url = GITHUB_LINK_ISSUE % {
        'project': 'weechat',
        'issue': match.group(2),
    }
    return f'<a href="{url}">{name}</a>'


def _replace_savannah_link(match):
    """Replace a match of Savannah keyword (like "bug #12345") by URL."""
    if match.group(1) not in SAVANNAH_LINKS:
        return match.group(0)
    name = match.group(0)
    url = SAVANNAH_LINKS[match.group(1)] % match.group(2)
    return f'<a href="{url}">{name}</a>'


def _replace_link(tracker):
    """Replace GitHub and Savannah links in a string."""
    string = GITHUB_ISSUE_PATTERN.sub(_replace_github_link, tracker)
    return SAVANNAH_ISSUE_PATTERN.sub(_replace_savannah_link, string)


def tracker_links(tracker):
    """Replace tracker items by URLs.

    Replace GitHub tracker item(s) (for example: "closes #123")
    and savannah tracker item(s) (for example: "bug #12345")
    by URL(s) to this/these item(s).
    """
    if not tracker:
        return ''
    items = [_replace_link(item) for item in tracker.split(',')]
    return mark_safe('<br>'.join(items))


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

    # read SVG with git commit/branch
    filename = project_path_join('templates', 'svg', 'git-commit.html')
    with open(filename, 'r', encoding='utf-8') as _file:
        svg_commit = _file.read().strip()
    filename = project_path_join('templates', 'svg', 'git-branch.html')
    with open(filename, 'r', encoding='utf-8') as _file:
        svg_branch = _file.read().strip()

    images = []
    for commit in commits.split(','):
        objtype = 'commit'
        link = svg_commit
        if commit.startswith('commit/'):
            commit = commit[7:]
        if commit.startswith('tree/'):
            objtype = 'tree'
            commit = commit[5:]
            link = svg_branch
        repo, commit_id = split_commit(commit)
        images.append(f'<a href="https://github.com/{repo}/{objtype}/{commit_id}">'
                      f'{link}</a>')
    return mark_safe(' '.join(images))


def repo_link_file(project, ref, filename):
    """Return link to a file in a given version on GitHub."""
    return GITHUB_LINK_FILE % {
        'project': project,
        'ref': ref,
        'filename': filename,
    }


def repo_link_release(project, version):
    """Return link to a release on GitHub."""
    return GITHUB_LINK_RELEASE % {
        'project': project,
        'version': version,
    }
