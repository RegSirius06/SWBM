from django import forms

from messenger.models import message

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
