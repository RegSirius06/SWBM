from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.passwords import is_valid_password

class ReNewPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        super(ReNewPasswordForm, self).__init__(*args, **kwargs)
        if password: self.valid_pass = password

    valid_pass = None
    new_pass = None

    old_pass = forms.CharField(max_length=40, label="Старый пароль:")

    def clean_old_pass(self):
        password = self.cleaned_data["old_pass"]
        if self.valid_pass and not self.valid_pass.check_password(password):
            raise ValidationError(_('Вы ввели неверный пароль.'))
        return password

    new_pass = forms.CharField(max_length=40, label="Новый пароль:")

    def clean_new_pass(self):
        self.new_pass =  self.cleaned_data["new_pass"]
        e = is_valid_password(self.new_pass)
        if e == True: return self.new_pass
        raise ValidationError(e)

    new_pass_again = forms.CharField(max_length=40, label="Подтверждение нового пароля:")

    def clean_new_pass_again(self):
        np = self.cleaned_data["new_pass_again"]
        if not self.new_pass: self.new_pass = self.cleaned_data["new_pass"]
        if np != self.new_pass:
            raise ValidationError(_('Введённые новые пароли не совпадают.'))
        return np
