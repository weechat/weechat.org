# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2018 Sébastien Helleu <flashcode@flashtux.org>
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

"""Models for "themes" menu."""

import gzip
from hashlib import md5
from io import open
import os
import re
import tarfile
from xml.sax.saxutils import escape

from django import forms
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy

from weechat.common.decorators import disable_for_loaddata
from weechat.common.forms import (
    CharField,
    ChoiceField,
    EmailField,
    FileField,
    TestField,
    Html5EmailInput,
    Form,
    getxmlline,
    getjsonline,
)
from weechat.common.path import files_path_join
from weechat.download.models import Release

MAX_LENGTH_NAME = 64
MAX_LENGTH_VERSION = 32
MAX_LENGTH_MD5SUM = 256
MAX_LENGTH_DESC = 1024
MAX_LENGTH_COMMENT = 1024
MAX_LENGTH_AUTHOR = 256
MAX_LENGTH_MAIL = 256


class Theme(models.Model):
    """A WeeChat theme."""
    visible = models.BooleanField(default=False)
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    version = models.CharField(max_length=MAX_LENGTH_VERSION)
    md5sum = models.CharField(max_length=MAX_LENGTH_MD5SUM, blank=True)
    desc = models.CharField(max_length=MAX_LENGTH_DESC, blank=True)
    comment = models.CharField(max_length=MAX_LENGTH_COMMENT, blank=True)
    author = models.CharField(max_length=MAX_LENGTH_AUTHOR)
    mail = models.CharField(max_length=MAX_LENGTH_MAIL)
    added = models.DateTimeField()
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return '%s - %s (%s, %s)' % (self.name, self.author, self.version,
                                     self.added)

    def __unicode__(self):  # python 2.x
        return self.__str__()

    def short_name(self):
        """Return short name (without extension)."""
        pos = self.name.find('.')
        if pos > 0:
            return self.name[0:pos]
        return self.name

    def path(self):
        """Return path to theme (for URL)."""
        pending = ''
        if not self.visible:
            pending = '/pending'
        return 'themes%s' % pending

    def html_preview(self):
        """Return HTML with theme preview."""
        filename = files_path_join('themes', 'html',
                                   os.path.basename('%s.html' % self.name))
        if os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as _file:
                content = _file.read()
            return content
        return ''

    def desc_i18n(self):
        """Return translated description."""
        return gettext_lazy(self.desc) if self.desc else ''

    def build_url(self):
        """Return URL to the theme."""
        return '/files/%s/%s' % (self.path(), self.name)

    def file_exists(self):
        """Checks if the theme exists (on disk)."""
        return os.path.isfile(files_path_join(self.path(),
                                              os.path.basename(self.name)))

    @staticmethod
    def get_props(themestring):
        """Get theme properties (from header in file)."""
        props = {}
        for line in themestring.split('\n'):
            line = str(line.strip().decode('utf-8'))
            if line.startswith('#'):
                match = re.match('^# \\$([A-Za-z]+): (.*)', line)
                if match:
                    props[match.group(1)] = match.group(2)
        return props

    class Meta:
        ordering = ['-added']


class ThemeFormAdd(Form):
    """Form to add a theme."""
    required_css_class = 'required'
    themefile = FileField(
        label=gettext_lazy('File'),
        help_text=gettext_lazy('The theme.'),
        widget=forms.FileInput(attrs={'autofocus': True}),
    )
    description = CharField(
        required=False,
        max_length=MAX_LENGTH_DESC,
        label=gettext_lazy('Description'),
    )
    author = CharField(
        max_length=MAX_LENGTH_AUTHOR,
        label=gettext_lazy('Your name or nick'),
        help_text=gettext_lazy('Used for themes page.'),
    )
    mail = EmailField(
        max_length=MAX_LENGTH_MAIL,
        label=gettext_lazy('Your e-mail'),
        help_text=gettext_lazy('No spam, never displayed.'),
        widget=Html5EmailInput(),
    )
    comment = CharField(
        required=False,
        max_length=1024,
        label=gettext_lazy('Comments'),
        help_text=gettext_lazy('Not displayed.'),
        widget=forms.Textarea(attrs={'rows': '3'}),
    )
    test = TestField(
        max_length=64,
        label=gettext_lazy('Are you a spammer?'),
        help_text=gettext_lazy('Enter "no" if you are not a spammer.'),
    )

    def __init__(self, *args, **kwargs):
        super(ThemeFormAdd, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    def clean_themefile(self):
        """Check if theme file is valid."""
        _file = self.cleaned_data['themefile']
        if _file.size > 512*1024:
            raise forms.ValidationError(gettext_lazy('Theme file too big.'))
        props = Theme.get_props(_file.read())
        if 'name' not in props or 'weechat' not in props:
            raise forms.ValidationError(gettext_lazy('Invalid theme file.'))
        themes = Theme.objects.filter(name=props['name'])
        if themes:
            raise forms.ValidationError(
                gettext_lazy('This name already exists.'))
        if not props['name'].endswith('.theme'):
            raise forms.ValidationError(
                gettext_lazy('Invalid name inside theme file.'))
        shortname = props['name'][0:-6]
        if not re.search('^[A-Za-z0-9_]+$', shortname):
            raise forms.ValidationError(
                gettext_lazy('Invalid name inside theme file.'))
        release_stable = Release.objects.get(version='stable')
        release_devel = Release.objects.get(version='devel')
        if props['weechat'] not in (release_stable.description,
                                    re.sub('-.*', '',
                                           release_devel.description)):
            raise forms.ValidationError(
                gettext_lazy('Invalid WeeChat version, too old!'))
        _file.seek(0)
        return _file


def get_theme_choices():
    """Get list of themes for update form."""
    try:
        theme_list = Theme.objects.filter(visible=1).order_by('name')
        theme_choices = []
        theme_choices.append(('', gettext_lazy('Choose...')))
        for theme in theme_list:
            theme_choices.append((theme.id, '%s (%s)' % (theme.name,
                                                         theme.version)))
        return theme_choices
    except:  # noqa: E722
        return []


class ThemeFormUpdate(Form):
    """Form to update a theme."""
    required_css_class = 'required'
    theme = ChoiceField(
        choices=[],
        label=gettext_lazy('Theme'),
        widget=forms.Select(attrs={'autofocus': True}),
    )
    themefile = FileField(
        label=gettext_lazy('File'),
        help_text=gettext_lazy('The theme.'),
    )
    author = CharField(
        max_length=MAX_LENGTH_AUTHOR,
        label=gettext_lazy('Your name or nick'),
    )
    mail = EmailField(
        max_length=MAX_LENGTH_MAIL,
        label=gettext_lazy('Your e-mail'),
        help_text=gettext_lazy('No spam, never displayed.'),
        widget=Html5EmailInput(),
    )
    comment = CharField(
        required=False,
        max_length=1024,
        label=gettext_lazy('Comments'),
        help_text=gettext_lazy('Not displayed.'),
        widget=forms.Textarea(attrs={'rows': '3'}),
    )
    test = TestField(
        max_length=64,
        label=gettext_lazy('Are you a spammer?'),
        help_text=gettext_lazy('Enter "no" if you are not a spammer.'),
    )

    def __init__(self, *args, **kwargs):
        super(ThemeFormUpdate, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['theme'].choices = get_theme_choices()

    def clean_themefile(self):
        """Check if theme file is valid."""
        _file = self.cleaned_data['themefile']
        if _file.size > 512*1024:
            raise forms.ValidationError(gettext_lazy('Theme file too big.'))
        props = Theme.get_props(_file.read())
        if 'name' not in props or 'weechat' not in props:
            raise forms.ValidationError(gettext_lazy('Invalid theme file.'))
        theme = Theme.objects.get(id=self.cleaned_data['theme'])
        if not theme:
            raise forms.ValidationError(gettext_lazy('Internal error.'))
        if props['name'] != theme.name:
            raise forms.ValidationError(
                gettext_lazy('Invalid name: different from theme.'))
        release_stable = Release.objects.get(version='stable')
        release_devel = Release.objects.get(version='devel')
        if props['weechat'] not in (release_stable.description,
                                    re.sub('-.*', '',
                                           release_devel.description)):
            raise forms.ValidationError(
                gettext_lazy('Invalid WeeChat version, too old!'))
        _file.seek(0)
        return _file


def xml_value(key, value):
    """Get a XML line for a key/value."""
    return '<%s>%s</%s>' % (
        key, value.replace('<', '&lt;').replace('>', '&gt;'), key)


def json_value(key, value):
    """Get a JSON line for a key/value."""
    return '"%s": "%s",' % (
        key, value.replace('"', '\\"').replace("'", "\\'"))


@disable_for_loaddata
def handler_theme_changed(sender, **kwargs):
    """Build files themes.{xml,json}(.gz) after update/delete of a theme."""
    theme_list = Theme.objects.filter(visible=1).order_by('id')
    xml = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml += '<themes>\n'
    json = '[\n'
    for theme in theme_list:
        if theme.visible:
            xml += '  <theme id="%s">\n' % theme.id
            json += '  {\n'
            json += '    "id": "%s",\n' % theme.id
            for key, value in theme.__dict__.items():
                if key not in ['_state', 'id', 'visible', 'comment']:
                    if value is None:
                        value = ''
                    else:
                        if key == 'mail':
                            value = value.replace('@', ' [at] ')
                            value = value.replace('.', ' [dot] ')
                        elif key == 'md5sum':
                            try:
                                with open(files_path_join(theme.path(),
                                                          theme.name),
                                          'rb') as _file:
                                    filemd5 = md5()
                                    filemd5.update(_file.read())
                                    value = filemd5.hexdigest()
                            except:  # noqa: E722
                                value = ''
                        elif key.startswith('desc'):
                            value = escape(value)
                    strvalue = '%s' % value
                    xml += getxmlline(key, strvalue)
                    json += getjsonline(key, strvalue)
            # FIXME: use the "Host" from request, but...
            # request is not available in this handler!
            strvalue = 'https://weechat.org/%s' % theme.build_url()[1:]
            xml += '    %s\n' % xml_value('url', strvalue)
            json += '    %s\n' % json_value('url', strvalue)
            xml += '  </theme>\n'
            json = json[:-2] + '\n  },\n'
    xml += '</themes>\n'
    json = json[:-2] + '\n]\n'

    # create themes.xml
    filename = files_path_join('themes.xml')
    with open(filename, 'w', encoding='utf-8') as _file:
        _file.write(xml)

    # create themes.xml.gz
    with open(filename, 'rb') as _f_in:
        _f_out = gzip.open(filename + '.gz', 'wb')
        _f_out.writelines(_f_in)
        _f_out.close()

    # create themes.json
    filename = files_path_join('themes.json')
    with open(filename, 'w', encoding='utf-8') as _file:
        _file.write(json)

    # create themes.json.gz
    with open(filename, 'rb') as _f_in:
        _f_out = gzip.open(filename + '.gz', 'wb')
        _f_out.writelines(_f_in)
        _f_out.close()

    # create themes.tar.bz2 (with theme.xml + 'themes' directory)
    os.chdir(settings.FILES_ROOT)
    tar = tarfile.open(files_path_join('themes.tar.bz2'), 'w:bz2')
    tar.add('themes.xml')
    for name in os.listdir(files_path_join('themes')):
        if name.endswith('.theme'):
            tar.add('themes/%s' % name)
    tar.close()


post_save.connect(handler_theme_changed, sender=Theme)
post_delete.connect(handler_theme_changed, sender=Theme)
