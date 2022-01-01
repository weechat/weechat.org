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

"""Models for "doc" menu."""

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext, gettext_noop

from weechat.common.i18n import i18n_autogen
from weechat.common.templatetags.localdate import localdate
from weechat.common.tracker import commits_links, tracker_links


CVE_URL = ('<a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=%(cve)s" '
           'target="_blank" rel="noopener">%(cve)s</a>')

SECURITY_SEVERITIES = (
    # Translators: this is a severity level for a security vulnerability
    (0, gettext_noop('low')),
    # Translators: this is a severity level for a security vulnerability
    (1, gettext_noop('medium')),
    # Translators: this is a severity level for a security vulnerability
    (2, gettext_noop('high')),
    # Translators: this is a severity level for a security vulnerability
    (3, gettext_noop('critical')),
)
SECURITY_SEVERITIES_DESC = {
    0: gettext_noop('minor issue occuring in very specific conditions, '
                    'low impact. Upgrade is not mandatory.'),
    1: gettext_noop('problem affecting a specific feature. Upgrade is '
                    '<strong>recommended</strong> at least for people using '
                    'the feature.'),
    2: gettext_noop('severe problem. Upgrade is '
                    '<strong>highly recommended</strong>.'),
    3: gettext_noop('critical problem, risk of damage on your system. '
                    '<strong>You MUST upgrade immediately!</strong>'),
}


class Language(models.Model):
    """A language with at least one translated doc."""
    LANG_I18N = {
        'cs': gettext_noop('Czech'),
        'de': gettext_noop('German'),
        'en': gettext_noop('English'),
        'es': gettext_noop('Spanish'),
        'fr': gettext_noop('French'),
        'hu': gettext_noop('Hungarian'),
        'it': gettext_noop('Italian'),
        'ja': gettext_noop('Japanese'),
        'pl': gettext_noop('Polish'),
        'pt': gettext_noop('Portuguese'),
        'pt_BR': gettext_noop('Portuguese (Brazil)'),
        'ru': gettext_noop('Russian'),
        'sr': gettext_noop('Serbian'),
        'tr': gettext_noop('Turkish'),
    }
    lang = models.CharField(max_length=8, primary_key=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.lang} ({self.priority})'

    def lang_i18n(self):
        """Return the translated language."""
        return gettext(self.LANG_I18N[self.lang])

    class Meta:
        ordering = ['priority']


class Version(models.Model):
    """A version for docs."""
    version = models.CharField(max_length=32, primary_key=True)
    priority = models.IntegerField(default=0)
    directory = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.version

    class Meta:
        ordering = ['priority']


class Doc(models.Model):
    """A WeeChat document file."""
    NAME_I18N = {
        'faq': gettext_noop('FAQ'),
        'user': gettext_noop('User\'s guide'),
        'plugin_api': gettext_noop('Plugin API reference'),
        'scripting': gettext_noop('Scripting guide'),
        'quickstart': gettext_noop('Quick Start guide'),
        'tester': gettext_noop('Tester\'s guide'),
        'dev': gettext_noop('Developer\'s guide'),
        'relay_protocol': gettext_noop('Relay protocol'),
    }
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    devel = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.version}, {self.priority})'

    def name_i18n(self):
        """Return the translated doc name."""
        return gettext(self.NAME_I18N[self.name])

    class Meta:
        ordering = ['priority']


class Security(models.Model):
    """A security vulnerability in WeeChat."""
    visible = models.BooleanField(default=True)
    date = models.DateTimeField()
    external = models.CharField(max_length=1024, blank=True)
    tracker = models.CharField(max_length=64, blank=True)
    severity = models.IntegerField(default=0, choices=SECURITY_SEVERITIES)
    affected = models.CharField(max_length=64, blank=True)
    fixed = models.CharField(max_length=32, blank=True)
    release_date = models.DateField(blank=True, null=True)
    commits = models.CharField(max_length=1024, blank=True)
    description = models.TextField()
    workaround = models.TextField(blank=True)

    def __str__(self):
        return (f'{self.external}, {self.tracker}, {self.severity}, '
                f'{self.affected} / {self.fixed}, {self.release_date}, '
                f'{self.description}')

    def date_l10n(self):
        """Return the date formatted with localized date format."""
        return localdate(self.date)

    def external_links(self):
        """Return URL to CVE (or "external" as-is if it's not a CVE)."""
        if self.external.startswith('CVE'):
            return CVE_URL % {'cve': self.external}
        return self.external

    def url_tracker(self):
        """Return URL with links to tracker items."""
        return tracker_links(self.tracker)

    def severity_i18n(self):
        """Return translated severity."""
        text = dict(SECURITY_SEVERITIES).get(self.severity, '')
        return gettext(text) if text else ''

    def severity_description_i18n(self):
        """Return translated severity."""
        text = SECURITY_SEVERITIES_DESC.get(self.severity, '')
        return gettext(text) if text else ''

    def severity_html_indicator(self):
        """Return HTML code for security indicator."""
        content = []
        content.append('<div class="d-inline-flex align-middle '
                       'severity-flex">')
        for i in range(0, 4):
            css_class = '' if self.severity < i else f' severity{i}'
            content.append(f'<div class="flex-fill severity{css_class}">'
                           f'</div>')
        content.append('</div>')
        return ''.join(content)

    def css_class(self):
        """Return the CSS class for the severity."""
        css_class = {
            0: 'light',
            1: 'secondary',
            2: 'warning',
            3: 'danger',
        }
        return css_class[self.severity]

    def affected_html(self):
        """Return affected versions for display in HTML."""
        return self.affected.replace(',', ' &rarr; ')

    def release_date_l10n(self):
        """Return the release date formatted with localized date format."""
        return localdate(self.release_date)

    def url_commits(self):
        """Return URL with links to commits."""
        return commits_links(self.commits)

    def description_i18n(self):
        """Return the translated description."""
        if self.description:
            return gettext(self.description.replace('\r\n', '\n'))
        return ''

    def workaround_i18n(self):
        """Return translated workaround."""
        if self.workaround:
            return gettext(self.workaround.replace('\r\n', '\n'))
        return ''

    class Meta:
        ordering = ['-date']


def handler_security_saved(sender, **kwargs):
    """Write file _i18n_security.py with security issues to translate."""
    # pylint: disable=unused-argument
    strings = []
    for security in Security.objects.filter(visible=1).order_by('-date'):
        if security.description:
            strings.append(security.description)
        if security.workaround:
            strings.append(security.workaround)
    i18n_autogen('doc', 'security', strings)


post_save.connect(handler_security_saved, sender=Security)
