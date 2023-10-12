import os

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants.bank.models import EXISTING_GROUPS
from constants.bank.forms import EXISTING_TYPES

class NewAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['save_and_new'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label="Тип аккаунта:")

    def clean_type_(self):
        return self.cleaned_data['type_']

    first_name = forms.CharField(label="Имя:")

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label="Отчество:")

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label="Фамилия:")

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    user_group = forms.ChoiceField(choices=EXISTING_GROUPS, label="Группа занятий:")

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label="Номер отряда:")

    def clean_party(self):
        return self.cleaned_data['party']

class NewAccountFullForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['save_and_new'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label="Тип аккаунта:")

    def clean_type_(self):
        return self.cleaned_data['type_']

    first_name = forms.CharField(label="Имя:")

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label="Отчество:")

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label="Фамилия:")

    def clean_last_name(self):
        return self.cleaned_data['last_name']
    
    username = forms.CharField(label="Login:")

    def clean_username(self):
        return self.cleaned_data['username']
    
    password = forms.CharField(label="Password:")

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) != 8 and len(password) != 12:
            raise ValidationError(_('Длина пароля должна быть равной 8-ми символам для пионера и 12-ти символам для педагога.'))
        return password

    user_group = forms.ChoiceField(choices=EXISTING_GROUPS, label="Группа занятий:")

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label="Номер отряда:")

    def clean_party(self):
        return self.cleaned_data['party']

class ReNewAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    first_name = forms.CharField(label="Имя:")

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label="Отчество:")

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label="Фамилия:")

    def clean_last_name(self):
        return self.cleaned_data['last_name']
    
    balance = forms.IntegerField(label="Баланс:")

    def clear_balance(self):
        return self.cleaned_data['balance']

    username = forms.CharField(label="Login:")

    def clean_username(self):
        return self.cleaned_data['username']

    user_group = forms.ChoiceField(choices=EXISTING_GROUPS, label="Группа занятий:")

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label="Номер отряда:")

    def clean_party(self):
        return self.cleaned_data['party']

class ReadFromFileForm(forms.Form):
    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label="Тип аккаунта:")

    def clean_type_(self):
        return self.cleaned_data['type_']

    way_to_file = forms.CharField(label="Путь к файлу (с названием файла):", required=False)

    def clean_way_to_file(self):
        x = self.cleaned_data['way_to_file']
        if x == "": return None
        y = os.path.split(x)
        if y[-1].split('.')[1] != 'txt' and y[-1].split('.')[1] != 'csv':
            raise ValidationError(_('Расширение файла должно быть .txt или .csv'))
        return x
