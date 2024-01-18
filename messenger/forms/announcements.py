from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bank.models import account
from constants.constants import PICTURE_TYPES, get_const_messenger_forms as gc

class NewAnnouncementForm(forms.Form):
    name = forms.CharField(max_length=50, label=gc("announcement, NewAnnouncementForm, fields, name, label"))

    def clean_name(self):
        return self.cleaned_data["name"]

    text = forms.CharField(label=gc("announcement, NewAnnouncementForm, fields, text, label"), max_length=5000, widget=forms.Textarea)

    def clean_text(self):
        return self.cleaned_data["text"]

    picture = forms.ImageField(label=gc("announcement, NewAnnouncementForm, fields, picture, label"),
                               widget=forms.ClearableFileInput, required=False)

    def clean_picture(self):
        picture = self.cleaned_data["picture"]
        if picture:
            def_text = gc("announcement, NewAnnouncementForm, methods, clean_picture")
            max_size = def_text[0] * 1024 * 1024
            if picture.size > max_size:
                raise ValidationError(_(f"{def_text[1]} - {max_size/1024/1024}{def_text[2]}"))
        return picture

class NewAnnouncementFullForm(NewAnnouncementForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_order = ('name', 'creator', 'text', 'picture', 'type_')

    creator = forms.ModelChoiceField(queryset=account.objects.all(),
                                     label=gc("announcement, NewAnnouncementFullForm, fields, creator, label"))

    def clean_creator(self):
        return self.cleaned_data["creator"]

    type_ = forms.ChoiceField(required=False, choices=PICTURE_TYPES,
                              label=gc("announcement, NewAnnouncementFullForm, fields, type_, label"),
                              help_text=gc("announcement, NewAnnouncementFullForm, fields, type_, help_text"))

    def clean_type_(self):
        x = self.cleaned_data['type_']
        return int(x) if x else 0

class ReNewAnnouncementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    status = forms.BooleanField(label=gc("announcement, ReNewAnnouncementForm, fields, status, label"), required=False)

    def clean_name(self):
        return self.cleaned_data["status"]

    creator = forms.ModelChoiceField(queryset=account.objects.all(),
                                     label=gc("announcement, ReNewAnnouncementForm, fields, creator, label"))

    def clean_creator(self):
        return self.cleaned_data["creator"]
