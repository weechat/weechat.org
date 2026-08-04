# SPDX-FileCopyrightText: 2003-2026 Sébastien Helleu <flashcode@flashtux.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
