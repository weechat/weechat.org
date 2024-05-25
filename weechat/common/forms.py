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

"""Common classes/functions for forms."""

from django import forms
from django.utils.translation import gettext


class BootstrapBoundField(forms.BoundField):
    """BoundField for bootstrap."""

    def css_classes(self, extra_classes=None):
        return super().css_classes() + ' form-group row'

    # pylint: disable=arguments-differ
    def label_tag(self, contents=None, attrs=None, **kwargs):
        attrs = attrs or {}
        class_list = [
            attrs.get('class', ''),
            'col-12 col-md-3 col-lg-2 col-form-label',
        ]
        attrs['class'] = ' '.join(class_list).strip()
        return super().label_tag(contents, attrs, **kwargs)

    def build_widget_attrs(self, attrs, widget=None):
        attrs = attrs or {}
        class_list = [
            attrs.get('class', ''),
            'form-control',
        ]
        attrs['class'] = ' '.join(class_list).strip()
        return super().build_widget_attrs(attrs, widget)


class CharField(forms.CharField):
    """Char field in new script form."""

    def get_bound_field(self, form, field_name):
        return BootstrapBoundField(form, self, field_name)


class ChoiceField(forms.ChoiceField):
    """Choice field in new script form."""

    def get_bound_field(self, form, field_name):
        return BootstrapBoundField(form, self, field_name)


class EmailField(forms.EmailField):
    """E-mail field in new script form."""

    def get_bound_field(self, form, field_name):
        return BootstrapBoundField(form, self, field_name)


class FileField(forms.FileField):
    """File field in new script form."""

    def get_bound_field(self, form, field_name):
        return BootstrapBoundField(form, self, field_name)


class TestField(forms.CharField):
    """Anti-spam field in forms."""

    def clean(self, value):
        if not value:
            raise forms.ValidationError(gettext('This field is required.'))
        if value.lower() != 'no':
            raise forms.ValidationError(gettext('This field is required.'))
        return value

    def get_bound_field(self, form, field_name):
        return BootstrapBoundField(form, self, field_name)


class Html5EmailInput(forms.widgets.Input):
    """E-mail field (with HTML5 validator)."""
    input_type = 'email'


class Form(forms.Form):
    """Form with "as_div" method."""

    def as_div(self):
        "Return this form rendered as HTML <div>s."
        return self._html_output(
            normal_row=('<div%(html_class_attr)s class="form-group row">'
                        '%(label)s'
                        '<div class="col-12 col-md-9 col-lg-10">'
                        '%(field)s%(help_text)s'
                        '</div>'
                        '</div>'),
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)
