#
# Copyright (C) 2003-2023 Sébastien Helleu <flashcode@flashtux.org>
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
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_noop

from weechat.common.i18n import i18n_autogen
from weechat.common.templatetags.localdate import localdate
from weechat.common.tracker import commits_links, tracker_links


URL_CVE = {
    'MITRE': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=%(cve)s',
    'NVD': 'https://nvd.nist.gov/vuln/detail/%(cve)s',
}

URL_CVSS_VECTOR = (
    'https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?'
    'vector=%(vector)s&version=3.1'
)

URL_CWE = 'https://cwe.mitre.org/data/definitions/%(cwe)s.html'

SECURITY_SEVERITIES = (
    # Translators: this is a severity level for a security vulnerability
    (0, gettext_noop('none')),
    # Translators: this is a severity level for a security vulnerability
    (1, gettext_noop('low')),
    # Translators: this is a severity level for a security vulnerability
    (2, gettext_noop('medium')),
    # Translators: this is a severity level for a security vulnerability
    (3, gettext_noop('high')),
    # Translators: this is a severity level for a security vulnerability
    (4, gettext_noop('critical')),
)


def get_severity(score):
    """Get severity (integer from 0 to 4) from score."""
    for i, limit in enumerate([0, 3.9, 6.9, 8.9, 10.0]):
        if score <= limit:
            return i
    return 0


def get_score_bar(score):
    """Return score bar."""
    score = round(score)
    content = []
    content.append(
        '<div class="d-inline-flex align-middle severity-flex">'
    )
    for i in range(0, 10):
        severity = get_severity(i + 1)
        css_class = f' severity{severity}' if i < score else ''
        content.append(
            f'<div class="flex-fill severity{css_class}"></div>'
        )
    content.append('</div>')
    return ''.join(content)


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
    wsa = models.CharField(max_length=64)
    cve = models.CharField(max_length=64, blank=True)
    cwe_id = models.IntegerField(default=0)
    cwe_text = models.CharField(max_length=64)
    cvss_vector = models.CharField(max_length=64)
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1)
    tracker = models.CharField(max_length=64, blank=True)
    affected = models.CharField(max_length=64, blank=True)
    fixed = models.CharField(max_length=32, blank=True)
    release_date = models.DateField(blank=True, null=True)
    commits = models.CharField(max_length=1024, blank=True)
    scope = models.CharField(max_length=64)
    issue = models.TextField()
    description = models.TextField()
    mitigation = models.TextField(blank=True)
    credit = models.TextField(blank=True)

    def __str__(self):
        return f'{self.wsa}: [{self.scope}] {self.issue} ({self.release_date})'

    def date_l10n(self):
        """Return the date formatted with localized date format."""
        return localdate(self.date)

    def cve_valid(self):
        """Return True if the CVE is a valid CVE id."""
        return self.cve.startswith('CVE')

    def cve_links(self):
        """Return URLs for the CVE."""
        if not self.cve_valid():
            return {}
        return {
            name: url % {'cve': self.cve}
            for name, url in URL_CVE.items()
        }

    def cve_i18n_table(self):
        """Return CVE to display in table."""
        if not self.cve:
            return '-'
        if self.cve_valid():
            return self.cve
        return gettext('Pending')

    def cve_i18n(self):
        """Return CVE to display in detailed info."""
        if not self.cve:
            not_avail = gettext('Not available')
            return mark_safe(f'<span class="text-muted">{not_avail}</span>')
        if self.cve_valid():
            return self.cve
        return gettext('Pending')

    def cwe_i18n(self):
        """Return the translated vulnerability type."""
        if self.cwe_text:
            return gettext(self.cwe_text)
        return ''

    def url_cwe(self):
        """Return URL to CWE detail."""
        if self.cwe_id > 0:
            return URL_CWE % {'cwe': self.cwe_id}
        return ''

    def url_cvss_vector(self):
        """Return URL to CVSS vector detail."""
        if self.cvss_vector:
            return URL_CVSS_VECTOR % {'vector': self.cvss_vector}
        return ''

    def url_tracker(self):
        """Return URL with links to tracker items."""
        return mark_safe(tracker_links(self.tracker))

    def severity_index(self):
        """Return severity index based on CVSS score."""
        return get_severity(self.cvss_score)

    def severity_i18n(self):
        """Return translated severity based on CVSS score."""
        text = dict(SECURITY_SEVERITIES).get(self.severity_index(), '')
        return gettext(text) if text else ''

    def score_bar(self):
        """Return HTML code with score bar."""
        return mark_safe(get_score_bar(self.cvss_score))

    def affected_html(self):
        """Return list of affected versions, as HTML."""
        list_affected = []
        for version in self.affected.split(','):
            if '-' in version:
                version1, version2 = version.split('-', 1)
                list_affected.append(f'{version1} → {version2}')
            else:
                list_affected.append(version)
        return mark_safe(', '.join(list_affected))

    def fixed_html(self):
        """Return fixed version, as HTML."""
        return mark_safe(f'<span class="text-success fw-bold">'
                         f'{self.fixed}</span>')

    def release_date_l10n(self):
        """Return the release date formatted with localized date format."""
        return localdate(self.release_date)

    def url_commits(self):
        """Return URL(s) with links to commits, as HTML."""
        return commits_links(self.commits)

    def scope_i18n(self):
        """Return the translated scope."""
        if self.scope:
            return gettext(self.scope)
        return ''

    def issue_i18n(self):
        """Return the translated issue."""
        if self.issue:
            return gettext(self.issue)
        return ''

    def description_i18n(self):
        """Return the translated description."""
        if self.description:
            return mark_safe(gettext(self.description.replace('\r\n', '\n')))
        return ''

    def mitigation_i18n(self):
        """Return translated mitigation."""
        if self.mitigation:
            return mark_safe(gettext(self.mitigation.replace('\r\n', '\n')))
        return ''

    class Meta:
        ordering = ['-date']


def handler_security_saved(sender, **kwargs):
    """Write file _i18n_security.py with security issues to translate."""
    # pylint: disable=unused-argument
    strings = []
    for security in Security.objects.filter(visible=1).order_by('-date'):
        fields = (
            security.cwe_text,
            security.scope,
            security.issue,
            security.description,
            security.mitigation,
        )
        strings.extend([field for field in fields if field])
    i18n_autogen('doc', 'security', strings)


post_save.connect(handler_security_saved, sender=Security)
