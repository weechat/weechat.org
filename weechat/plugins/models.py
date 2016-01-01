# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2016 Sébastien Helleu <flashcode@flashtux.org>
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
# along with WeeChat.org.  If not, see <http://www.gnu.org/licenses/>.
#

"""Models for "scripts" menu."""

import gzip
from hashlib import md5
from os import path
import re
from xml.sax.saxutils import escape

from django import forms
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.forms.widgets import Input
from django.utils import translation
from django.utils.translation import ugettext, gettext_lazy, pgettext_lazy

from weechat.common.i18n import i18n_autogen
from weechat.common.path import files_path_join
from weechat.download.models import Release

SCRIPT_LANGUAGE = {
    'python': ('py', 'python'),
    'perl': ('pl', 'perl'),
    'ruby': ('rb', 'ruby'),
    'lua': ('lua', 'lua'),
    'tcl': ('tcl', 'tcl'),
    'guile': ('scm', 'scheme'),
    'javascript': ('js', 'javascript'),
}

MAX_LENGTH_NAME = 64
MAX_LENGTH_VERSION = 32
MAX_LENGTH_URL = 512
MAX_LENGTH_LANGUAGE = 32
MAX_LENGTH_LICENSE = 32
MAX_LENGTH_MD5SUM = 256
MAX_LENGTH_TAGS = 512
MAX_LENGTH_DESC = 1024
MAX_LENGTH_APPROVAL = 1024
MAX_LENGTH_REQUIRE = 512
MAX_LENGTH_AUTHOR = 256
MAX_LENGTH_MAIL = 256


def get_language_from_extension(ext):
    return next((key for key, value in SCRIPT_LANGUAGE.items()
                 if value[0] == ext), None)


class Plugin(models.Model):
    """A WeeChat script."""
    visible = models.BooleanField(default=False)
    popularity = models.IntegerField()
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    version = models.CharField(max_length=MAX_LENGTH_VERSION)
    url = models.CharField(max_length=MAX_LENGTH_URL, blank=True)
    language = models.CharField(max_length=MAX_LENGTH_LANGUAGE)
    license = models.CharField(max_length=MAX_LENGTH_LICENSE)
    md5sum = models.CharField(max_length=MAX_LENGTH_MD5SUM, blank=True)
    tags = models.CharField(max_length=MAX_LENGTH_TAGS, blank=True)
    desc_en = models.CharField(max_length=MAX_LENGTH_DESC)
    approval = models.CharField(max_length=MAX_LENGTH_APPROVAL, blank=True)
    requirements = models.CharField(max_length=MAX_LENGTH_REQUIRE, blank=True)
    min_weechat = models.CharField(max_length=MAX_LENGTH_VERSION, blank=True)
    max_weechat = models.CharField(max_length=MAX_LENGTH_VERSION, blank=True)
    author = models.CharField(max_length=MAX_LENGTH_AUTHOR)
    mail = models.EmailField(max_length=MAX_LENGTH_MAIL)
    added = models.DateTimeField()
    updated = models.DateTimeField()

    def __unicode__(self):
        api = ''
        if self.max_weechat == '0.2.6':
            api = '(legacy api) '
        return '%s %s %s(%s, %s)' % (self.name, self.version, api,
                                     self.author, self.added)

    def tagslist(self):
        """Return a list with script tags."""
        return self.tags.split(',')

    def path(self):
        """Return path to script (for URL)."""
        pending = ''
        if not self.visible:
            pending = '/pending'
        if self.max_weechat == '0.2.6':
            return 'scripts/legacy%s' % pending
        else:
            return 'scripts%s' % pending

    def popularity_img(self):
        """Return HTML code with image for popular script."""
        if self.popularity == 0:
            return '&nbsp;'
        return ('<img src="%simages/star.png" alt="*" title="%s" '
                'width="10" height="10" />' %
                (settings.MEDIA_URL,
                 gettext_lazy('Popular script')))

    def name_with_extension(self):
        """Return the name of script with its extension."""
        return '%s.%s' % (self.name, SCRIPT_LANGUAGE[self.language][0])

    def extension(self):
        """Return script extension."""
        return SCRIPT_LANGUAGE[self.language][0]

    def language_display(self):
        """Return script language."""
        return SCRIPT_LANGUAGE[self.language][1]

    def desc_i18n(self):
        """Return translated description."""
        return gettext_lazy(self.desc_en.encode('utf-8'))

    def version_weechat(self):
        """Return the min/max WeeChat versions in a string."""
        wee_min = self.min_weechat
        if wee_min == '':
            wee_min = '0.0.1'
        if self.max_weechat == '':
            return '%s+' % wee_min
        else:
            return '%s-%s' % (wee_min, self.max_weechat)

    def version_weechat_html(self):
        """Return the min/max WeeChat versions in a string for HTML."""
        wee_min = self.min_weechat
        if wee_min == '':
            wee_min = '0.0.1'
        if self.max_weechat == '':
            return '&ge; %s' % wee_min
        else:
            return '%s &rarr; %s' % (wee_min, self.max_weechat)

    def build_url(self):
        """Return URL to the script."""
        return '/files/%s/%s' % (self.path(), self.name_with_extension())

    def filename(self):
        """Return script filename (on disk)."""
        return files_path_join(self.path(),
                               path.basename(self.name_with_extension()))

    def file_exists(self):
        """Check if script exists (on disk)."""
        return path.isfile(self.filename())

    def md5(self):
        """Return MD5 checksum of script."""
        try:
            with open(self.filename(), 'rb') as _file:
                filemd5 = md5()
                filemd5.update(_file.read())
                return filemd5.hexdigest()
        except:
            return ''

    class Meta:
        ordering = ['-added']


class NameField(forms.CharField):
    """Name field in new script form."""
    def clean(self, value):
        if not value:
            raise forms.ValidationError(
                gettext_lazy('This field is required.'))
        if not re.search('^[a-z0-9_]+$', value):
            raise forms.ValidationError(
                gettext_lazy('This name is invalid.'))
        plugins = Plugin.objects.exclude(max_weechat='0.2.6') \
            .filter(name=value)
        if plugins:
            raise forms.ValidationError(
                gettext_lazy('This name already exists, please choose another '
                             'name (update script content accordingly).'))
        if len(value) > 20:
            raise forms.ValidationError(
                gettext_lazy('This name is too long (must be max 20 chars).'))
        return value


class TestField(forms.CharField):
    """Anti-spam field in forms."""
    def clean(self, value):
        if not value:
            raise forms.ValidationError(
                gettext_lazy('This field is required.'))
        if value.lower() != 'no':
            raise forms.ValidationError(
                gettext_lazy('This field is required.'))
        return value


class Html5EmailInput(Input):
    """E-mail field (with HTML5 validator)."""
    input_type = 'email'


def get_min_max_choices():
    """Get min/max versions for add form."""
    try:
        version_min_max = []
        devel_desc = Release.objects.get(version='devel').description
        releases = Release.objects.filter(
            version__gte='0.3.0',
            version__lte=re.sub('-.*', '', devel_desc)).order_by('date')
        for rel in releases:
            version_min_max.append(
                (
                    '%s:-' % rel.version,
                    '≥ %s'.decode('utf-8') % rel.version,
                    ))
        return version_min_max
    except:
        return []


class PluginFormAdd(forms.Form):
    """Form to add a script."""
    languages = (
        ('python', 'Python (.py)'),
        ('perl', 'Perl (.pl)'),
        ('ruby', 'Ruby (.rb)'),
        ('lua', 'Lua (.lua)'),
        ('tcl', 'Tcl (.tcl)'),
        ('guile', 'Scheme (.scm)'),
        ('javascript', 'Javascript (.js)'),
    )
    required_css_class = 'required'
    language = forms.ChoiceField(
        choices=languages,
        label=pgettext_lazy(u'programming language', u'Language')
    )
    name = NameField(
        max_length=MAX_LENGTH_NAME,
        label=gettext_lazy('Name'),
        help_text=gettext_lazy('short name of script (max 20 chars, only '
                               'lower case letters, digits or "_")'),
        widget=forms.TextInput(attrs={'size': '10'})
    )
    version = forms.CharField(
        max_length=MAX_LENGTH_VERSION,
        label=gettext_lazy('Version'),
        help_text=gettext_lazy('version of script (only digits or dots)'),
        widget=forms.TextInput(attrs={'size': '7'})
    )
    license = forms.CharField(
        max_length=MAX_LENGTH_LICENSE,
        label=gettext_lazy('License'),
        help_text=gettext_lazy('license (for example: GPL3, BSD, ...)'),
        widget=forms.TextInput(attrs={'size': '7'})
    )
    file = forms.FileField(
        label=gettext_lazy('File'),
        help_text=gettext_lazy('the script')
    )
    description = forms.CharField(
        max_length=MAX_LENGTH_DESC,
        label=gettext_lazy('Description'),
        widget=forms.TextInput(attrs={'size': '60'})
    )
    requirements = forms.CharField(
        required=False,
        max_length=MAX_LENGTH_REQUIRE,
        label=gettext_lazy('Requirements'),
        help_text=gettext_lazy('optional'),
        widget=forms.TextInput(attrs={'size': '30'})
    )
    min_max = forms.ChoiceField(
        choices=[],
        label=gettext_lazy('Min/max WeeChat')
    )
    author = forms.CharField(
        max_length=MAX_LENGTH_AUTHOR, label=gettext_lazy('Your name or nick'),
        help_text=gettext_lazy('used for scripts page and git commit')
    )
    mail = forms.EmailField(
        max_length=MAX_LENGTH_MAIL,
        label=gettext_lazy('Your e-mail'),
        help_text=gettext_lazy('used for scripts page and git commit'),
        widget=Html5EmailInput(attrs={'size': '40'})
    )
    comment = forms.CharField(
        required=False,
        max_length=1024,
        label=gettext_lazy('Comments'),
        help_text=gettext_lazy('optional, not displayed'),
        widget=forms.Textarea(attrs={'rows': '3'})
    )
    test = TestField(
        max_length=64,
        label=gettext_lazy('Are you a spammer?'),
        help_text=gettext_lazy('enter "no" if you are not a spammer'),
        widget=forms.TextInput(attrs={'size': '10'})
    )

    def __init__(self, *args, **kwargs):
        super(PluginFormAdd, self).__init__(*args, **kwargs)
        self.fields['min_max'].choices = get_min_max_choices()


def get_plugin_choices():
    """Get list of scripts for update form."""
    try:
        plugin_list = Plugin.objects.exclude(max_weechat='0.2.6') \
            .filter(visible=1).order_by('name')
        plugin_choices = []
        plugin_choices.append(('', gettext_lazy('Choose...')))
        for plugin in plugin_list:
            name = '%s - v%s (%s)' % (plugin.name_with_extension(),
                                      plugin.version, plugin.version_weechat())
            plugin_choices.append((plugin.id, name))
        return plugin_choices
    except:
        return []


class PluginFormUpdate(forms.Form):
    """Form to update a script."""
    required_css_class = 'required'
    plugin = forms.ChoiceField(
        choices=[],
        label=gettext_lazy('Script')
    )
    version = forms.CharField(
        max_length=MAX_LENGTH_VERSION,
        label=gettext_lazy('New version'),
        widget=forms.TextInput(attrs={'size': '10'})
    )
    file = forms.FileField(
        label=gettext_lazy('File'),
        help_text=gettext_lazy('the script')
    )
    author = forms.CharField(
        max_length=MAX_LENGTH_AUTHOR,
        label=gettext_lazy('Your name or nick'),
        help_text=gettext_lazy('used for git commit')
    )
    mail = forms.EmailField(
        max_length=MAX_LENGTH_MAIL,
        label=gettext_lazy('Your e-mail'),
        help_text=gettext_lazy('used for git commit'),
        widget=Html5EmailInput(attrs={'size': '40'})
    )
    comment = forms.CharField(
        max_length=1024,
        label=gettext_lazy('Comments'),
        help_text=gettext_lazy('changes in this release'),
        widget=forms.Textarea(attrs={'rows': '3'})
    )
    test = TestField(
        max_length=64,
        label=gettext_lazy('Are you a spammer?'),
        help_text=gettext_lazy('enter "no" if you are not a spammer'),
        widget=forms.TextInput(attrs={'size': '10'})
    )

    def __init__(self, *args, **kwargs):
        super(PluginFormUpdate, self).__init__(*args, **kwargs)
        self.fields['plugin'].choices = get_plugin_choices()


def getxmlline(key, value):
    """Get a XML line for a key/value."""
    strvalue = '%s' % value
    return '    <%s>%s</%s>\n' % (
        key, strvalue.replace('<', '&lt;').replace('>', '&gt;'), key)


def getjsonline(key, value):
    """Get a JSON line for a key/value."""
    strvalue = '%s' % value
    return '    "%s": "%s",\n' % (
        key, strvalue.replace('"', '\\"').replace("'", "\\'"))


def handler_plugin_changed(sender, **kwargs):
    """Build files plugins.{xml,json}(.gz) after update/delete of a script."""
    xml = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml += '<plugins>\n'
    json = '[\n'
    strings = []
    for plugin in Plugin.objects.filter(visible=1).order_by('id'):
        if plugin.visible:
            xml += '  <plugin id="%s">\n' % plugin.id
            json += '  {\n'
            json += '    "id": "%s",\n' % plugin.id
            for key, value in plugin.__dict__.items():
                value_i18n = {}
                if key not in ['_state', 'id', 'visible', 'approval']:
                    if value is None:
                        value = ''
                    else:
                        if key == 'url':
                            # FIXME: use the "Host" from request, but...
                            # request is not available in this handler!
                            value = ('http://weechat.org/%s' %
                                     plugin.build_url()[1:])
                        elif key == 'mail':
                            value = value.replace('@', ' [at] ')
                            value = value.replace('.', ' [dot] ')
                        elif key == 'md5sum':
                            value = plugin.md5()
                        elif key.startswith('desc'):
                            if key == 'desc_en':
                                for lang, locale in \
                                        settings.LANGUAGES_LOCALES.items():
                                    if lang[0:2] != 'en':
                                        translation.activate(lang)
                                        value_i18n['desc_%s' % locale] = \
                                            escape(ugettext(value))
                                        translation.deactivate()
                            value = escape(value)
                    xml += getxmlline(key, value)
                    json += getjsonline(key, value)
                    for field in value_i18n:
                        xml += getxmlline(field, value_i18n[field])
                        json += getjsonline(field, value_i18n[field])
            xml += '  </plugin>\n'
            json += '  },\n'
            strings.append(
                (
                    plugin.desc_en,
                    'description for script "%s" (%s)' % (
                        plugin.name_with_extension(),
                        plugin.version_weechat()),
                ))
    xml += '</plugins>\n'
    json = json[:-2]
    json += '\n]\n'

    # create plugins.xml
    filename = files_path_join('plugins.xml')
    with open(filename, 'w') as _file:
        _file.write(xml.encode('utf-8'))

    # create plugins.xml.gz
    with open(filename, 'rb') as _f_in:
        _f_out = gzip.open(filename + '.gz', 'wb')
        _f_out.writelines(_f_in)
        _f_out.close()

    # create plugins.json
    filename = files_path_join('plugins.json')
    with open(filename, 'w') as _file:
        _file.write(json.encode('utf-8'))

    # create plugins.json.gz
    with open(filename, 'rb') as _f_in:
        _f_out = gzip.open(filename + '.gz', 'wb')
        _f_out.writelines(_f_in)
        _f_out.close()

    # create _i18n_plugins.py
    i18n_autogen('plugins', 'plugins', strings)

post_save.connect(handler_plugin_changed, sender=Plugin)
post_delete.connect(handler_plugin_changed, sender=Plugin)
