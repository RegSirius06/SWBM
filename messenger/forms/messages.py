from typing import Any
from django import forms

from messenger.models import message

class NewMessageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        messages = kwargs.pop('messages', None)
        super(NewMessageForm, self).__init__(*args, **kwargs)
        if messages:
            choice_list = [(None, '-' * 30)]
            for i in messages:
                choice_list.append((f"{i.id}", f"{i.decrypt_data()}"[:20] + ('...' if len(i.decrypt_data()) >= 20 else '')))
            self.fields['message_citate'].choices = choice_list

    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']

    message_anonim = forms.BooleanField(initial=False, required=False, label="Анонимно?", help_text="Если вы хотите отправить сообщение анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['message_anonim']
    
    message_citate = forms.ChoiceField(choices=(), required=False, label="Ответить на:", help_text="Выберите сообщение, на которое вы хотите ответить: ")

    def clean_messahe_citate(self):
        return self.cleaned_data['message_citate']

class NewMessageForm_WithoutAnonim(forms.Form):
    def __init__(self, *args, **kwargs):
        messages = kwargs.pop('messages', None)
        super(NewMessageForm_WithoutAnonim, self).__init__(*args, **kwargs)
        if messages:
            choice_list = [(None, '-' * 30)]
            for i in messages:
                choice_list.append((f"{i.id}", f"{i.decrypt_data()}"[:20] + ('...' if len(i.decrypt_data()) >= 20 else '')))
            self.fields['message_citate'].choices = choice_list

    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']
    
    message_citate = forms.ChoiceField(choices=(), required=False, label="Ответить на:", help_text="Выберите сообщение, на которое вы хотите ответить: ")

    def clean_messahe_citate(self):
        return self.cleaned_data['message_citate']

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

class ResendMessageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        chats = kwargs.pop('chats', None)
        chat = kwargs.pop('chat', None)
        super(ResendMessageForm, self).__init__(*args, **kwargs)
        choice_list = [('None', 'Глобальный чат')] if chat else []
        if chats:
            for i in chats:
                if i != chat: choice_list.append((f"{i.id}", f"{i.name}"))
        self.fields['chats'].choices = choice_list
    
    chats = forms.MultipleChoiceField(choices=(), required=False, label="Выберите чат, в который хотите переслать сообщение:")

    def clean_chats(self):
        x = self.cleaned_data['chats']
        x = [i if i != 'None' else None for i in x]
        return x
