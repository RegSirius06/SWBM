from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bank.models import account
from messenger.models import chat, chat_valid
from messenger.forms.other import ImageSelectWidget
from constants.constants import CONFLICT_SOLVES, get_const_messenger_forms as gc

class SetReadStatusForm(forms.Form):
    pass

class NewChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(NewChatForm, self).__init__(*args, **kwargs)
        if current_user is not None:
            self.fields['chat_members'].queryset = account.objects.exclude(pk=current_user.pk)

    chat_name = forms.CharField(label=gc("chats, NewChatForm, fields, chat_name, label"))

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        if f'{name}' in chat_all: raise ValidationError(_(gc("chats, NewChatForm, methods, clean_chat_name")))
        return name
    
    chat_description = forms.CharField(label=gc("chats, NewChatForm, fields, chat_description, label"), widget=forms.Textarea)

    def clean_chat_description(self):
        return self.cleaned_data['chat_description']
    
    image_list = [f'{i}.png' for i in range(7)]
    image_choice = forms.ChoiceField(label=gc("chats, NewChatForm, fields, image_choice, label"), required=False,
                                     choices=[(img, img) for img in image_list], widget=ImageSelectWidget())

    def clean_image_choice(self):
        img = self.cleaned_data['image_choice']
        if img is None or img == '': img = self.image_list[0]
        return img

    chat_resend = forms.BooleanField(initial=True, required=False, help_text=gc("chats, NewChatForm, fields, chat_resend, help_text"),
                                     label=gc("chats, NewChatForm, fields, chat_resend, label"))

    def clean_chat_resend(self):
            return self.cleaned_data['chat_resend']

    chat_anonim = forms.BooleanField(initial=False, required=False, help_text=gc("chats, NewChatForm, fields, chat_anonim, help_text"),
                                     label=gc("chats, NewChatForm, fields, chat_anonim, label"))

    def clean_chat_anonim(self):
        return self.cleaned_data['chat_anonim']

    chat_anonim_legacy = forms.BooleanField(initial=False, required=False,
                                            label=gc("chats, NewChatForm, fields, chat_anonim_legacy, label"),
                                            help_text=gc("chats, NewChatForm, fields, chat_anonim_legacy, help_text"))

    def clean_chat_anonim_legacy(self):
        return self.cleaned_data['chat_anonim_legacy']

    chat_members = forms.ModelMultipleChoiceField(queryset=account.objects.all(),
                                                  label=gc("chats, NewChatForm, fields, chat_members, label"),
                                                  help_text=gc("chats, NewChatForm, fields, chat_members, help_text"))

    def clean_chat_members(self):
        members = self.cleaned_data['chat_members']
        #def_text = gc("chats, NewChatForm, methods, clean_chat_members")
        #if len(list(members)) > def_text[0]:
        #    raise ValidationError(_(def_text[1]))
        return members

class NewChatFormConflict(forms.Form):
    solve = forms.ChoiceField(choices=CONFLICT_SOLVES, label=gc("chats, NewChatFormConflict, fields, solve, label"))

    def clean_type_(self):
        return self.cleaned_data['solve']

class ReNewChatFormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        current_user = kwargs.pop('current_user', None)
        self_id = kwargs.pop('self_id', None)
        super().__init__(*args, **kwargs)
        self._self_id = self_id
        if current_users is not None:
            current_users_pk = [i.id for i in current_users]
            self.fields['chat_creator'].queryset = account.objects.filter(id__in=current_users_pk)
            self.fields['chat_members'].queryset = account.objects.exclude(id__in=current_users_pk)
            if current_user is not None: self.fields['chat_creator'].queryset = account.objects.filter(id__in=current_users_pk).exclude(pk=current_user.pk)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    chat_creator = forms.ModelChoiceField(queryset=account.objects.all(), required=False,
                                          label=gc("chats, ReNewChatFormBase, fields, chat_creator, label"),
                                          help_text=gc("chats, ReNewChatFormBase, fields, chat_creator, help_text"))

    def clean_chat_creator(self):
        return self.cleaned_data['chat_creator']

    image_list = [f'{i}.png' for i in range(7)]
    image_choice = forms.ChoiceField(label=gc("chats, ReNewChatFormBase, fields, image_choice, label"), required=False,
                                     choices=[(img, img) for img in image_list], widget=ImageSelectWidget())

    def clean_image_choice(self):
        x = self.cleaned_data['image_choice']
        if not x: x = self.image_list[0]
        return x

    chat_name = forms.CharField(label=gc("chats, ReNewChatFormBase, fields, chat_name, label"))

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        chat_all = [f'{i.name}' for i in chat.objects.exclude(id=self._self_id) if chat_valid.objects.get(what_chat=i).avaliable]
        if f'{name}' in chat_all: raise ValidationError(_(gc("chats, ReNewChatFormBase, methods, clean_chat_name")))
        return name

    chat_text = forms.CharField(widget=forms.Textarea, label=gc("chats, ReNewChatFormBase, fields, chat_text, label"))

    def clean_chat_text(self):
        return self.cleaned_data['chat_text']
    
    chat_resend = forms.BooleanField(required=False, help_text=gc("chats, ReNewChatFormBase, fields, chat_resend, help_text"),
                                     label=gc("chats, ReNewChatFormBase, fields, chat_resend, label"))

    def clean_chat_resend(self):
            return self.cleaned_data['chat_resend']

    chat_members = forms.ModelMultipleChoiceField(queryset=account.objects.all(), required=False,
                                                  label=gc("chats, ReNewChatFormBase, fields, chat_members, label"),
                                                  help_text=gc("chats, ReNewChatFormBase, fields, chat_members, help_text"))

    def clean_chat_members(self):
        members = self.cleaned_data['chat_members']
        def_text = gc("chats, ReNewChatFormBase, fields, chat_creator, label")
        #if len(list(members)) > def_text[0]:
        #    raise ValidationError(_(def_text[1]))
        return members

class ReNewChatFormAnonim(ReNewChatFormBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_order = ('chat_creator', 'image_choice', 'chat_name', 'chat_text', 'chat_anonim', 'chat_resend', 'chat_members')

    chat_anonim = forms.BooleanField(required=False, label=gc("chats, ReNewChatFormAnonim, fields, chat_anonim, label"),
                                     help_text=gc("chats, ReNewChatFormAnonim, fields, chat_anonim, help_text"))

    def clean_message_anonim(self):
        return self.cleaned_data['chat_anonim']
