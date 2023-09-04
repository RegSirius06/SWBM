from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bank.models import account
from messenger.models import chat, chat_valid
from messenger.forms.other import ImageSelectWidget

class SetReadStatusForm(forms.Form):
    pass

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
    
    image_list = [f'{i}.png' for i in range(7)]
    image_choice = forms.ChoiceField(label="Аватарка чата:", required=False, choices=[(img, img) for img in image_list], widget=ImageSelectWidget())

    def clean_image_choice(self):
        img = self.cleaned_data['image_choice']
        if img is None or img == '': img = self.image_list[0]
        return img

    chat_anonim = forms.BooleanField(initial=False, required=False, help_text="Если вы хотите сделать чат анонимным, поставьте здесь галочку.\nЭтот параметр неизменяем.", label="Чат анонимный?")

    def clean_chat_anonim(self):
        return self.cleaned_data['chat_anonim']

    chat_anonim_legacy = forms.BooleanField(initial=False, required=False, label="Анонимные сообщения?", help_text="Если вы хотите разрешить отправку анонимных сообщений, вы должны поставить галочку.\nЭтот параметр неизменяем, не влияет на анонимный чат.")

    def clean_chat_anonim_legacy(self):
        return self.cleaned_data['chat_anonim_legacy']

    chat_members = forms.ModelMultipleChoiceField(queryset=account.objects.all(), label="Участники чата:", help_text="Выберите участника(-ов) чата.")

    def clean_chat_members(self):
        members = self.cleaned_data['chat_members']
        #if len(list(members)) > 25:
        #    raise ValidationError(_('В чате не может быть больше 25-ти человек. Если вы хотите создать чат с большим количеством людей, вам нужно обратиться к администратору.'))
        return members

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

    image_list = [f'{i}.png' for i in range(7)]
    image_choice = forms.ChoiceField(label="Аватарка чата:", choices=[(img, img) for img in image_list], widget=ImageSelectWidget())

    def clean_image_choice(self):
        return self.cleaned_data['image_choice']

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

    image_list = [f'{i}.png' for i in range(7)]
    image_choice = forms.ChoiceField(label="Аватарка чата:", choices=[(img, img) for img in image_list], widget=ImageSelectWidget())

    def clean_image_choice(self):
        return self.cleaned_data['image_choice']

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        #chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        #if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name

    chat_text = forms.CharField(widget=forms.Textarea, label="Описание чата:")

    def clean_chat_text(self):
        return self.cleaned_data['chat_text']
