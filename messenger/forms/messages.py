from django import forms

from constants.constants import get_const_messenger_forms as gc

class NewMessageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        messages = kwargs.pop('messages', None)
        super().__init__(*args, **kwargs)
        if messages:
            choice_list = [(None, '-' * 30)]
            for i in messages:
                choice_list.append((f"{i.id}", f"{i.decrypt_data()}"[:20] + ('...' if len(i.decrypt_data()) >= 20 else '')))
            self.fields['message_citate'].choices = choice_list

    message_text = forms.CharField(widget=forms.Textarea, help_text=gc("messages, NewMessageForm, fields, message_text, help_text"),
                                   label=gc("messages, NewMessageForm, fields, message_text, label"))

    def clean_message_text(self):
        return self.cleaned_data['message_text']

    message_anonim = forms.BooleanField(initial=False, required=False,
                                        label=gc("messages, NewMessageForm, fields, message_anonim, label"),
                                        help_text=gc("messages, NewMessageForm, fields, message_anonim, help_text"))

    def clean_message_anonim(self):
        return self.cleaned_data['message_anonim']
    
    message_citate = forms.ChoiceField(choices=(), required=False, label=gc("messages, NewMessageForm, fields, message_citate, label"),
                                       help_text=gc("messages, NewMessageForm, fields, message_citate, help_text"))

    def clean_messahe_citate(self):
        return self.cleaned_data['message_citate']

class NewMessageForm_WithoutAnonim(NewMessageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["message_anonim"]
        fields_order = ('message_text', 'message_anonim')

class ReNewMessageFormAnonim(NewMessageForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            del self.fields["message_citate"]
            fields_order = ('message_text', 'message_anonim')
            self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

class ReNewMessageFormBase(ReNewMessageFormAnonim):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["message_anonim"]

class ResendMessageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        chats = kwargs.pop('chats', None)
        chat = kwargs.pop('chat', None)
        super().__init__(*args, **kwargs)
        choice_list = [("None", gc("messages, ResendMessageForm, methods, __init__"))] if chat else []
        if chats:
            for i in chats:
                if i != chat: choice_list.append((f"{i.id}", f"{i.name}"))
        self.fields['chats'].choices = choice_list
    
    chats = forms.MultipleChoiceField(choices=(), required=False, label=gc("messages, ResendMessageForm, fields, chats, label"))

    def clean_chats(self):
        x = self.cleaned_data['chats']
        x = [i if i != 'None' else None for i in x]
        return x
