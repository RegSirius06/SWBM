import uuid

from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bank.models import account, good, rools
from constants.constants import SIGN_SET, SIGN_SET_ALL, DATE_START_OF_, DATE_END_OF_, get_const_bank_forms as gc

class NewTransactionRoolBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields["transaction_receiver"].queryset = account.objects.exclude(party=0).order_by('party', 'last_name')
    
    transaction_receiver = forms.ModelMultipleChoiceField(queryset=None,\
                           label=gc('transactions, NewTransactionBaseForm, fields, transaction_receiver, label'))

    def clean_transaction_receiver(self):
        return self.cleaned_data['transaction_receiver']

class NewTransactionRoolForm(NewTransactionRoolBaseForm):
    rool = forms.ModelChoiceField(queryset=rools.objects.filter(Q(cost__gt=0)), label='Пункт:')

    def clean_rool(self):
        return self.cleaned_data['rool']

class NewTransactionBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields["transaction_receiver"].queryset = account.objects.exclude(party=0).order_by('party', 'last_name')
    
    transaction_receiver = forms.ModelChoiceField(queryset=None,\
                           label=gc('transactions, NewTransactionBaseForm, fields, transaction_receiver, label'))

    def clean_transaction_receiver(self):
        return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text=gc('transactions, NewTransactionBaseForm, fields, transaction_cnt, help_text'),\
                                       label=gc('transactions, NewTransactionBaseForm, fields, transaction_cnt, label'))

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_(gc('transactions, NewTransactionBaseForm, methods, clean_transaction_cnt')))
        return cnt

    transaction_comment = forms.CharField(help_text=gc('transactions, NewTransactionBaseForm, fields, transaction_comment, help_text'),\
                                          label=gc('transactions, NewTransactionBaseForm, fields, transaction_comment, label'))

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']

class NewTransactionStaffForm(NewTransactionBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["transaction_receiver"].choices =\
            tuple([(x.id, f"{x}") for x in account.objects.exclude(party=0).order_by('party', 'last_name')])
        fields_order = ('transaction_date', 'transaction_receiver', 'transaction_cnt',\
                        'transaction_comment', 'transaction_sign')

    transaction_receiver = forms.MultipleChoiceField(choices=[],\
                           label=gc('transactions, NewTransactionStaffForm, fields, transaction_receiver, label'))

    def clean_transaction_receiver(self):
        list_x = list(self.cleaned_data['transaction_receiver'])
        return account.objects.filter(id__in=list_x)

    transaction_date = forms.DateField(help_text=gc('transactions, NewTransactionStaffForm, fields, transaction_date, help_text'),\
                                       label=gc('transactions, NewTransactionStaffForm, fields, transaction_date, label'))

    def clean_transaction_date(self):
        v_e_ = gc('transactions, NewTransactionStaffForm, methods, clean_transaction_date')
        data = self.cleaned_data['transaction_date']
        if data < DATE_START_OF_:
            raise ValidationError(_(v_e_[0]))
        if data > DATE_END_OF_:
            raise ValidationError(_(v_e_[1]))
        return data

    transaction_sign = forms.ChoiceField(choices=SIGN_SET,\
                                         help_text=gc('transactions, NewTransactionStaffForm, fields, transaction_sign, help_text'),\
                                            label=gc('transactions, NewTransactionStaffForm, fields, transaction_sign, label'))
    
    def clean_transaction_sign(self):
        return self.cleaned_data['transaction_sign']

class NewTransactionStaffFormParty(NewTransactionStaffForm):
    transaction_receiver = forms.IntegerField(label=gc('transactions, NewTransactionStaffFormParty, fields, transaction_receiver, label'),\
                           help_text=gc('transactions, NewTransactionStaffFormParty, fields, transaction_receiver, help_text'))
    
    def clean_transaction_receiver(self):
            v_e_ = gc('transactions, NewTransactionStaffFormParty, methods, clean_transaction_receiver')
            list_accounts = {i.party for i in account.objects.all() if i.party != 0}
            x = int(self.cleaned_data['transaction_receiver'])
            if x <= 0:
                raise ValidationError(_(v_e_[0]))
            if x not in list_accounts:
                raise ValidationError(_(v_e_[1]))
            return x

class NewTransactionFullForm(NewTransactionStaffForm):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        super().__init__(*args, **kwargs)
        fields_order = ('transaction_date', 'transaction_creator', 'transaction_receiver', 'transaction_history',\
                        'transaction_cnt', 'transaction_comment', 'transaction_sign')
        self.fields["transaction_sign"].choices = SIGN_SET_ALL
        if current_users is not None:
            self.fields['transaction_creator'].queryset = account.objects.exclude(id__in=current_users)

    transaction_creator = forms.ModelChoiceField(queryset=account.objects.all(),\
                          label=gc('transactions, NewTransactionFullForm, fields, transaction_creator, label'))#, widget=forms.RadioSelect()) 
    
    def clean_transaction_creator(self):
            return self.cleaned_data['transaction_creator']

    transaction_history = forms.ModelChoiceField(queryset=account.objects.all(),\
                          label=gc('transactions, NewTransactionFullForm, fields, transaction_history, label'))#, widget=forms.RadioSelect()) 

    def clean_transaction_history(self):
            return self.cleaned_data['transaction_history']

class NewTransactionBuyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        goods = good.objects.all()
        for gd in goods:
            self.fields[f"good_{gd.id}"] = forms.IntegerField(label=gd.name, initial=0)

    def clean_goods(self):
        cleaned_data = super().clean()
        dt = {}
        ls = []
        for field_name, value in cleaned_data.items():
            if field_name.startswith('good_'):
                good_id = field_name.split('_')[1]
                gd = good.objects.get(id=good_id)
                dt[gd] = value
                ls.append(uuid.UUID(good_id))
        return [dt, ls]
    
    list_accounts = account.objects.exclude(party=0).order_by('party', 'last_name')
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts,\
                           label=gc('transactions, NewTransactionBuyForm, fields, transaction_receiver, label'))#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']
    
class ReNewTransactionStaffForm(NewTransactionStaffForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["transaction_receiver"]
        fields_order = ('transaction_date', 'transaction_history', 'transaction_cnt',\
                        'transaction_comment', 'transaction_sign')
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
        self.fields['edit'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    transaction_history = forms.ModelChoiceField(queryset=account.objects.all(),\
                          label=gc('transactions, ReNewTransactionStaffForm, fields, transaction_history, label'))#, widget=forms.RadioSelect()) 

    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_history']
