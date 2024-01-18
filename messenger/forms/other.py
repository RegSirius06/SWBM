from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from constants.constants import EXISTING_THEMES, get_const_messenger_forms as gc

class ImageSelectWidget(forms.RadioSelect):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for option_value, option_label in self.choices:
            image_path = f'messenger/images/{option_value}'  # Путь до изображения
            image_url = static(image_path)
            image_tag = format_html('<img src="{}" alt="{}" style="width: 50px; height: 50px;" />', image_url, option_label)
            label_tag = format_html(
                '<label for="{}">{} {}</label>',
                attrs['id'], format_html('<input type="radio" name="{}" value="{}" />', name, option_value), image_tag
            )
            output.append(format_html('<div>{}</div>', label_tag))
        return mark_safe('\n'.join(output))

class SetStatus(forms.Form):
    status = forms.CharField(max_length=50, required=False, label=gc("other, SetStatus, fields, status, label"))

    def clean_status(self):
        return self.cleaned_data['status']

class ReNewThemeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        selected = kwargs.pop('selected', None)
        super().__init__(*args, **kwargs)
        self.fields['type_'].initial = selected if selected else 'default'

    type_ = forms.ChoiceField(required=False, choices=EXISTING_THEMES, help_text=gc("other, ReNewThemeForm, fields, type_, help_text"),
                              label=gc("other, ReNewThemeForm, fields, type_, label"))

    def clean_type_(self):
        return self.cleaned_data['type_']
