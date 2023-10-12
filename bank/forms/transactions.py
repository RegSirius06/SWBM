import uuid

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bank.models import account, good
from constants.bank.forms import SIGN_SET, SIGN_SET_ALL
from constants.bank.forms import DATE_START_OF_, DATE_END_OF_

class NewTransactionStaffForm(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < DATE_START_OF_:
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > DATE_END_OF_:
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    list_accounts = account.objects.exclude(party=0)
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts, label="Получатель:")#, widget=forms.RadioSelect()) 

    def clean_transaction_receiver(self):
        return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']

class NewTransactionStaffFormParty(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < DATE_START_OF_:
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > DATE_END_OF_:
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    transaction_receiver = forms.IntegerField(label="Получатель:", help_text="Введите номер отряда.")
    
    def clean_transaction_receiver(self):
            list_accounts = set([i.party for i in account.objects.all() if i.party != 0])
            x = int(self.cleaned_data['transaction_receiver'])
            if x <= 0:
                raise ValidationError(_('Вы не можете выбрать служебные отряды.'))
            if x not in list_accounts:
                raise ValidationError(_('Такого отряда не существует.'))
            return x

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']

class NewTransactionFullForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        super(NewTransactionFullForm, self).__init__(*args, **kwargs)
        if current_users is not None:
            self.fields['transaction_creator'].queryset = account.objects.exclude(id__in=current_users)
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < DATE_START_OF_:
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > DATE_END_OF_:
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    list_accounts = account.objects.exclude(party=0)
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts, label="Получатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']
    
    transaction_creator = forms.ModelChoiceField(queryset=account.objects.all(), label="Даватель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_creator(self):
            return self.cleaned_data['transaction_creator']
    
    transaction_history = forms.ModelChoiceField(queryset=account.objects.all(), label="Создатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_history(self):
            return self.cleaned_data['transaction_history']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=SIGN_SET_ALL, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']

class NewTransactionBuyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewTransactionBuyForm, self).__init__(*args, **kwargs)
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
    
    list_accounts = account.objects.exclude(party=0)
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts, label="Покупатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']
    
class ReNewTransactionStaffForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
        self.fields['edit'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    transaction_history = forms.ModelChoiceField(queryset=account.objects.all(), label="Создатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_history']

    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < DATE_START_OF_:
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > DATE_END_OF_:
            raise ValidationError(_('Вы указали дату после смены.'))
        return data

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']

class NewTransactionBaseForm(forms.Form):
    transaction_receiver = forms.ModelChoiceField(queryset=account.objects.exclude(party=0).order_by('party', 'last_name'), label="Получатель:")

    def clean_transaction_receiver(self):
        return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете перевести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение перевода.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
