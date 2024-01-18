from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants.constants import get_const_bank_forms as gc

class NewDailyAnswerAddForm(forms.Form):
    name = forms.CharField(max_length=40, label=gc('daily_answers, NewDailyAnswerAddForm, fields, name, label'))

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label=gc('daily_answers, NewDailyAnswerAddForm, fields, comment, label'), widget=forms.Textarea)

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label=gc('daily_answers, NewDailyAnswerAddForm, fields, cost, label'))

    def clean_cost(self):
        x = int(self.cleaned_data["cost"])
        if x <= 0:
            raise ValidationError(_(gc('daily_answers, NewDailyAnswerAddForm, methods, clean_cost')))
        return x

    giga_ans = forms.BooleanField(label=gc('daily_answers, NewDailyAnswerAddForm, fields, giga_ans, label'), initial=False, required=False)

    def clean_giga_ans(self):
        return int(self.cleaned_data["giga_ans"])

class ReNewDailyAnswerAddForm(NewDailyAnswerAddForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
