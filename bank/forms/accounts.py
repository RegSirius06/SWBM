import os

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants.constants import EXISTING_TYPES, EXISTING_GROUPS, get_const_bank_forms as gc

class __BaseAccountForm__(forms.Form):
    first_name = forms.CharField(label=gc("accounts, __BaseAccountForm__, fields, first_name, label"))

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label=gc("accounts, __BaseAccountForm__, fields, middle_name, label"))

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label=gc("accounts, __BaseAccountForm__, fields, last_name, label"))

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    user_group = forms.ChoiceField(choices=EXISTING_GROUPS, label=gc("accounts, __BaseAccountForm__, fields, user_group, label"))

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label=gc("accounts, __BaseAccountForm__, fields, party, label"))

    def clean_party(self):
        x = int(self.cleaned_data['party'])
        if x < 0:
            raise ValidationError(_(gc("accounts, __BaseAccountForm__, methods, clean_party")))
        return x

class NewAccountForm(__BaseAccountForm__):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_order = ('type_', 'first_name', 'middle_name', 'last_name', 'user_group', 'party')
        self.fields['save_and_new'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label=gc("accounts, NewAccountForm, fields, type_, label"))

    def clean_type_(self):
        return self.cleaned_data['type_']

class NewAccountFullForm(NewAccountForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_order = ('type_', 'first_name', 'middle_name', 'last_name', 'username', 'password', 'user_group', 'party')

    username = forms.CharField(label=gc("accounts, NewAccountFullForm, fields, username, label"))

    def clean_username(self):
        return self.cleaned_data['username']

    password = forms.CharField(label=gc("accounts, NewAccountFullForm, fields, password, label"))

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) != 8 and len(password) != 12:
            raise ValidationError(_(gc("accounts, NewAccountFullForm, methods, clean_password")))
        return password

class ReNewAccountForm(__BaseAccountForm__):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_order = ('first_name', 'middle_name', 'last_name', 'balance', 'username', 'user_group', 'party')
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    balance = forms.IntegerField(label=gc("accounts, ReNewAccountForm, fields, balance, label"))

    def clear_balance(self):
        return self.cleaned_data['balance']

    username = forms.CharField(label=gc("accounts, ReNewAccountForm, fields, username, label"))

    def clean_username(self):
        return self.cleaned_data['username']

class ReadFromFileForm(forms.Form):
    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label=gc("accounts, ReadFromFileForm, fields, type_, label"))

    def clean_type_(self):
        return self.cleaned_data['type_']

    way_to_file = forms.CharField(label=gc("accounts, ReadFromFileForm, fields, type_, label"), required=False)

    def clean_way_to_file(self):
        x = self.cleaned_data['way_to_file']
        if x == "": return None
        y = os.path.split(x)
        if y[-1].split('.')[-1] != 'txt' and y[-1].split('.')[-1] != 'csv':
            raise ValidationError(_(gc("accounts, ReadFromFileForm, methods, clean_way_to_file")))
        return x
