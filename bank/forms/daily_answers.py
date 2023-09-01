from django import forms

class NewDailyAnswerAddForm(forms.Form):
    name = forms.CharField(max_length=40, label="Название задачи:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Условие задачи:", widget=forms.Textarea)

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Награда:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

    giga_ans = forms.BooleanField(label="Это задача смены?", initial=False, required=False)

    def clean_giga_ans(self):
        return int(self.cleaned_data["giga_ans"])

class ReNewDailyAnswerAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    name = forms.CharField(max_length=40, label="Название задачи:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Условие задачи:", widget=forms.Textarea)

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Награда:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

    giga_ans = forms.BooleanField(label="Это задача смены?", required=False)

    def clean_giga_ans(self):
        return int(self.cleaned_data["giga_ans"])
