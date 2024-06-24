from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bank.models import account, rools
from constants.constants import SIGN_SET, get_const_bank_forms as gc

class NewAutoTransactionRoolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["accounts"].queryset = account.objects.exclude(party=0).order_by('party', 'last_name')

    accounts = forms.ModelMultipleChoiceField(queryset=account.objects.all(), label="На кого")

    def clean_accounts(self):
        x = self.cleaned_data['accounts']
        if [i for i in x] == []:
            raise ValidationError(_('Укажите хотя бы одного пользователя, к которому создаёте автотранзакцию.'))
        return x

    rool = forms.ModelChoiceField(queryset=rools.objects.filter(Q(cost__gt=0)), label='Пункт:')

    def clean_rool(self):
        return self.cleaned_data['rool']

    skip = forms.IntegerField(help_text="Сколько дней пропускать, считая сегодня?", label="Пропуски")

    def clean_skip(self):
        skip = int(self.cleaned_data['skip'])
        if skip < 0:
            raise ValidationError(_(gc('transactions, NewTransactionBaseForm, methods, clean_transaction_cnt')))
        return skip

class NewAutoTransactionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["accounts"].queryset = account.objects.exclude(party=0).order_by('party', 'last_name')

    accounts = forms.ModelMultipleChoiceField(queryset=account.objects.all(), label="На кого")

    def clean_accounts(self):
        x = self.cleaned_data['accounts']
        if [i for i in x] == []:
            raise ValidationError(_('Укажите хотя бы одного пользователя, к которому создаёте автотранзакцию.'))
        return x

    comment = forms.CharField(help_text=gc('transactions, NewTransactionBaseForm, fields, transaction_comment, help_text'),\
                                          label=gc('transactions, NewTransactionBaseForm, fields, transaction_comment, label'))

    def clean_comment(self):
        return self.cleaned_data['comment']

    sign = forms.ChoiceField(choices=SIGN_SET,
                             help_text=gc('transactions, NewTransactionStaffForm, fields, transaction_sign, help_text'),
                             label=gc('transactions, NewTransactionStaffForm, fields, transaction_sign, label'))
    
    def clean_sign(self):
        return self.cleaned_data['sign']

    cnt = forms.FloatField(help_text=gc('transactions, NewTransactionBaseForm, fields, transaction_cnt, help_text'),\
                                       label=gc('transactions, NewTransactionBaseForm, fields, transaction_cnt, label'))

    def clean_cnt(self):
        cnt = float(self.cleaned_data['cnt'])
        if cnt <= 0:
            raise ValidationError(_(gc('transactions, NewTransactionBaseForm, methods, clean_transaction_cnt')))
        return cnt

    skip = forms.IntegerField(help_text="Сколько дней пропускать, считая сегодня?", label="Пропуски")

    def clean_skip(self):
        skip = int(self.cleaned_data['skip'])
        if skip < 0:
            raise ValidationError(_(gc('transactions, NewTransactionBaseForm, methods, clean_transaction_cnt')))
        return skip

class ReNewAutoTransactionForm(NewAutoTransactionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
