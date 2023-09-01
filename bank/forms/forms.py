from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bank.models import account, transaction, message, rools, plan, daily_answer, good, chat, chat_and_acc, chat_valid
from django.core.paginator import Paginator
import datetime
import uuid

class SetStatus(forms.Form):
    status = forms.CharField(max_length=50, required=False, label="Введите новый статус:")

    def clean_status(self):
        return self.cleaned_data['status']

class SetReadStatusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NewMessageForm(forms.Form):
    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']

    message_anonim = forms.BooleanField(initial=False, required=False, label="Анонимно?", help_text="Если вы хотите отправить сообщение анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['message_anonim']
    
    class Meta:
        model = message
        fields = ['message_receiver', 'message_text', 'message_anonim']

class NewMessageForm_WithoutAnonim(forms.Form):
    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']
    
    class Meta:
        model = message
        fields = ['message_receiver', 'message_text', 'message_anonim']

class ReNewMessageFormAnonim(forms.Form):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']

    message_anonim = forms.BooleanField(initial=False, required=False, label="Анонимно?", help_text="Если вы хотите отправить сообщение анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['message_anonim']
    
    class Meta:
        model = message
        fields = ['message_text', 'message_anonim']

class ReNewMessageFormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']
    
    class Meta:
        model = message
        fields = ['message_text']

class NewChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(NewChatForm, self).__init__(*args, **kwargs)
        if current_user is not None:
            self.fields['chat_members'].queryset = account.objects.exclude(pk=current_user.pk)

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name
    
    chat_description = forms.CharField(label="Описание чата:")

    def clean_chat_description(self):
        return self.cleaned_data['chat_description']
    
    chat_anonim = forms.BooleanField(initial=False, required=False, help_text="Если вы хотите сделать чат анонимным, поставьте здесь галочку.\nЭтот параметр неизменяем.", label="Чат анонимный?")

    def clean_chat_anonim(self):
        return self.cleaned_data['chat_anonim']

    chat_anonim_legacy = forms.BooleanField(initial=False, required=False, label="Анонимные сообщения?", help_text="Если вы хотите разрешить отправку анонимных сообщений, вы должны поставить галочку.\nЭтот параметр неизменяем, не влияет на анонимный чат.")

    def clean_chat_anonim_legacy(self):
        return self.cleaned_data['chat_anonim_legacy']

    chat_members = forms.ModelMultipleChoiceField(queryset=account.objects.all(), label="Участники чата:", help_text="Выберите участников чата. (Вы будете в нём независимо от вашего выбора здесь.)")

    def clean_chat_members(self):
        return self.cleaned_data['chat_members']

class NewChatFormConflict(forms.Form):
    CONFLICT_SOLVES = (
        (0, "Создать новый чат и заархивировать существующий"),
        (1, "Не создавать новый чат, заархивировать существующий"),
        (2, "Не создавать новый чат, не архивировать существующий"),
    )

    solve = forms.ChoiceField(choices=CONFLICT_SOLVES, label="Действие:")

    def clean_type_(self):
        return self.cleaned_data['solve']

class ReNewChatFormAnonim(forms.Form):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        current_user = kwargs.pop('current_user', None)
        super(ReNewChatFormAnonim, self).__init__(*args, **kwargs)
        if current_users is not None:
            current_users_pk = [i.pk for i in current_users]
            self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk)
            if current_user is not None: self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk).exclude(pk=current_user.pk)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    chat_creator = forms.ModelChoiceField(queryset=account.objects.all(), required=False, label="Создатель:", help_text="Здесь вы можете изменить создателя чата. Это необязательно.")

    def clean_chat_creator(self):
        return self.cleaned_data['chat_creator']

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        #chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        #if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name

    chat_text = forms.CharField(widget=forms.Textarea, label="Описание чата:")

    def clean_chat_text(self):
        return self.cleaned_data['chat_text']

    chat_anonim = forms.BooleanField(required=False, label="Анонимные сообщения?", help_text="Если вы хотите разрешить отправку сообщения анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['chat_anonim']

class ReNewChatFormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        current_user = kwargs.pop('current_user', None)
        super(ReNewChatFormBase, self).__init__(*args, **kwargs)
        if current_users is not None:
            current_users_pk = [i.pk for i in current_users]
            self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk)
            if current_user is not None: self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk).exclude(pk=current_user.pk)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    chat_creator = forms.ModelChoiceField(queryset=account.objects.all(), required=False, label="Создатель:", help_text="Здесь вы можете изменить создателя чата. Это необязательно.")

    def clean_chat_creator(self):
        return self.cleaned_data['chat_creator']

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        #chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        #if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name

    chat_text = forms.CharField(widget=forms.Textarea, label="Описание чата:")

    def clean_chat_text(self):
        return self.cleaned_data['chat_text']

