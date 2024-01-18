from django import forms

class NewGoodAddForm(forms.Form):
    name = forms.CharField(max_length=40, label="Название:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Комментарий:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Цена:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

class ReNewGoodAddForm(NewGoodAddForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
