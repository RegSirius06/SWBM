from django import forms

class NewPlanAddForm(forms.Form):
    time = forms.CharField(max_length=40, label="Во сколько:")

    def clean_time(self):
        return self.cleaned_data["time"]

    comment = forms.CharField(label="Комментарий:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    number = forms.IntegerField(label="Номер в списке:")

    def clean_number(self):
        return int(self.cleaned_data["number"])

class ReNewPlanAddForm(NewPlanAddForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
