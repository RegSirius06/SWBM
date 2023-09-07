import os

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from messenger.models import announcement
from bank.models import account

class NewAnnouncementForm(forms.Form):
    name = forms.CharField(max_length=50, label="Название:")

    def clean_name(self):
        return self.cleaned_data["name"]

    text = forms.CharField(label="Текст:", max_length=5000, widget=forms.Textarea)

    def clean_text(self):
        return self.cleaned_data["text"]

    picture = forms.ImageField(label="Картинка:", widget=forms.ClearableFileInput, required=False)

    def clean_picture(self):
        picture = self.cleaned_data["picture"]
        if picture:
            max_size = 15 * 1024 * 1024
            if picture.size > max_size:
                raise ValidationError(_(f"Максимальный размер файла - {max_size/1024/1024}MB"))
        return picture

class NewAnnouncementFullForm(forms.Form):
    name = forms.CharField(max_length=50, label="Название:")

    def clean_name(self):
        return self.cleaned_data["name"]

    creator = forms.ModelChoiceField(queryset=account.objects.all(), label="Создатель:")

    def clean_creator(self):
        return self.cleaned_data["creator"]

    text = forms.CharField(label="Текст:", max_length=5000, widget=forms.Textarea)

    def clean_text(self):
        return self.cleaned_data["text"]
    
    picture = forms.ImageField(label="Картинка:", widget=forms.ClearableFileInput, required=False)

    def clean_picture(self):
        picture = self.cleaned_data["picture"]
        if picture:
            max_size = 15 * 1024 * 1024
            if picture.size > max_size:
                raise ValidationError(_(f"Максимальный размер файла - {max_size/1024/1024}MB"))
        return picture

    type_ = forms.ChoiceField(required=False, choices=announcement.PICTURE_TYPES, label="Тип ориентации картинки:", help_text="По-умолчанию горизонтально.")

    def clean_type_(self):
        x = self.cleaned_data['type_']
        return int(x) if x else 0

class ReNewAnnouncementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    status = forms.BooleanField(label="Объявление принято?", required=False)

    def clean_name(self):
        return self.cleaned_data["status"]

    creator = forms.ModelChoiceField(queryset=account.objects.all(), label="Создатель:")

    def clean_creator(self):
        return self.cleaned_data["creator"]
