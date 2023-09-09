from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from choice_of_path.forms import ReNewPasswordForm
from utils.passwords import is_valid_password

def index(request):
    return render(
        request,
        'choice_of_path/index.html',
        context={},
    )

def change_password(request):
    if request.method == 'POST':
        form = ReNewPasswordForm(request.POST, password=request.user)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            if request.user.check_password(old_pass):
                new_pass = form.cleaned_data['new_pass']
                if is_valid_password(new_pass) == True:
                    new_pass_again = form.cleaned_data['new_pass_again']
                    if new_pass == new_pass_again:
                        request.user.password = make_password(new_pass)
                        request.user.save()
            return redirect('index')
    else:
        form = ReNewPasswordForm(password=request.user)
    return render(
        request,
        'registration/password_change.html',
        {'form': form, 'head': 'Изменение объявления'},
    )
