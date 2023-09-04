import os
import uuid
import string
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse

from bank.models import account, transaction
from bank.forms import accounts
from utils import read_from

@permission_required('bank.staff_')
@permission_required('bank.edit_users')
def account_info(request):
    acc_all = account.objects.all()
    paginator1 = Paginator(acc_all, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'bank/accounts/account_status.html',
        context={
            'object_list': items1,
        }
    )

@permission_required('bank.staff_')
@permission_required('bank.register')
def new_account_add_from_file(request):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

    def gen_pass(length: int) -> str:
        lang = []
        hard_to_read = "l1IioO0"
        for i in string.printable[:62]:
            if i in hard_to_read: continue
            lang.append(i)
        list_ = []
        for u in User.objects.all():
            list_.append(u.password)
        set_list = set(list_)
        while True:
            pas = ""
            for i in range(length):
                el = random.choice(lang)
                pas += el
            if pas not in set_list:
                return pas

    if request.method == 'POST':
        form = accounts.ReadFromFileForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data['way_to_file']
            if s:
                if os.path.split(s)[-1].split('.')[-1] == 'txt': list_with_dict = read_from.from_txt(s)
                else: list_with_dict = read_from.from_csv(s)
            else: list_with_dict = read_from.from_txt()
            type_ = int(form.cleaned_data['type_'])
            for i in list_with_dict:
                new_account = account()

                first_name = i['i']
                middle_name = i['o']
                last_name = i['f']
                username = f'{translit(first_name[0])}.{translit(middle_name[0])}.{translit(last_name)}'
                for u in User.objects.all():
                    if f'{u.username}' == f'{username}':
                        print(u, username)
                        return HttpResponse("<h2>Такой пользователь уже существует. <a href=\"/\">Назад...</a></h2>")
                user_group = i['g']
                party = i['n']
                len_pass = 8 if type_ == 0 else 12
                password = gen_pass(len_pass)

                if f'{type_}' == '1':
                    group_, created = Group.objects.get_or_create(name="pedagogue")
                    if created:
                        perms, created = Permission.objects.get_or_create(codename="staff_")
                        group_.permissions.add(perms)
                        perms, created = Permission.objects.get_or_create(codename="transaction")
                        group_.permissions.add(perms)
                        perms, created = Permission.objects.get_or_create(codename="transaction_base")
                        group_.permissions.add(perms)
                        perms, created = Permission.objects.get_or_create(codename="meria")
                        group_.permissions.add(perms)
                        perms, created = Permission.objects.get_or_create(codename="edit_users")
                        group_.permissions.add(perms)
                        perms, created = Permission.objects.get_or_create(codename="ant_edit")
                        group_.permissions.add(perms)
                else: group_, created = Group.objects.get_or_create(name="listener")
                group_.save()
                group_meria, created = Group.objects.get_or_create(name="meria")
                if created:
                    perms, created = Permission.objects.get_or_create(codename="staff_")
                    group_meria.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="meria")
                    group_meria.permissions.add(perms)
                group_meria.save()
                
                new_user = User.objects.create(username=username, password=make_password(password))
                new_user.groups.add(group_)

                new_account.id = uuid.uuid4()
                new_account.user = new_user
                new_account.first_name = first_name
                new_account.middle_name = middle_name
                new_account.last_name = last_name
                new_account.user_group = user_group
                new_account.party = party
                new_account.balance = 0
                new_account.save()

                s_write = f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
                f = open("All_users.txt", "a")
                f.write(s_write)
                f.close()
            return redirect('info-users')
    else: form = accounts.ReadFromFileForm()
    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Импорт аккаунтов из файла",})

@permission_required('bank.staff_')
@permission_required('bank.register')
def new_account_add(request):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

    def gen_pass(length: int) -> str:
        lang = []
        hard_to_read = "l1IioO0"
        for i in string.printable[:62]:
            if i in hard_to_read: continue
            lang.append(i)
        list_ = []
        for u in User.objects.all():
            list_.append(u.password)
        set_list = set(list_)
        while True:
            pas = ""
            for i in range(length):
                el = random.choice(lang)
                pas += el
            if pas not in set_list:
                return pas

    if request.method == 'POST':
        form = accounts.NewAccountForm(request.POST)
        if form.is_valid():
            new_account = account()

            type_ = int(form.cleaned_data['type_'])
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            username = f'{translit(first_name[0])}.{translit(middle_name[0])}.{translit(last_name)}'
            for u in User.objects.all():
                if f'{u.username}' == f'{username}': return HttpResponse("<h2>Такой пользователь уже существует. <a href=\"/\">Назад...</a></h2>")
            user_group = form.cleaned_data['user_group']
            party = form.cleaned_data['party']
            len_pass = 8 if type_ == 0 else 12
            password = gen_pass(len_pass)

            if f'{type_}' == '1':
                group_, created = Group.objects.get_or_create(name="pedagogue")
                if created:
                    perms, created = Permission.objects.get_or_create(codename="staff_")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="transaction")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="transaction_base")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="meria")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="edit_users")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="ant_edit")
                    group_.permissions.add(perms)
            else: group_, created = Group.objects.get_or_create(name="listener")
            group_.save()
            group_meria, created = Group.objects.get_or_create(name="meria")
            if created:
                perms, created = Permission.objects.get_or_create(codename="staff_")
                group_meria.permissions.add(perms)
                perms, created = Permission.objects.get_or_create(codename="meria")
                group_meria.permissions.add(perms)
            group_meria.save()
            
            new_user = User.objects.create(username=username, password=make_password(password))
            new_user.groups.add(group_)

            new_account.id = uuid.uuid4()
            new_account.user = new_user
            new_account.first_name = first_name
            new_account.middle_name = middle_name
            new_account.last_name = last_name
            new_account.user_group = user_group
            new_account.party = party
            new_account.balance = 0
            new_account.save()

            s_write = f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
            f = open("All_users.txt", "a")
            f.write(s_write)
            f.close()

            if form.cleaned_data['save_and_new']:
                return redirect('new-user')
            else:
                return redirect('info-users')
    else:
        type_ = 0
        first_name = "Not stated"
        middle_name = "Not stated"
        last_name = "Not stated"
        user_group = None
        party = 0
        form = accounts.NewAccountForm(initial={'type_': type_, 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                                       'id': id, 'user_group': user_group, 'party': party})
    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Добавить новый аккаунт",})

@permission_required('bank.staff_')
@permission_required('bank.register')
def new_account_full_add(request):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

    if request.method == 'POST':
        form = accounts.NewAccountFullForm(request.POST)
        if form.is_valid():
            new_account = account()

            type_ = form.cleaned_data['type_']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            username = translit(form.cleaned_data['username'])
            for u in User.objects.all():
                if f'{u.username}' == f'{username}': return HttpResponse("<h2>Такой пользователь уже существует. <a href=\"/\">Назад...</a></h2>")
            user_group = form.cleaned_data['user_group']
            party = form.cleaned_data['party']
            password = form.cleaned_data['password']

            if f'{type_}' == '1':
                group_, created = Group.objects.get_or_create(name="pedagogue")
                if created:
                    perms, created = Permission.objects.get_or_create(codename="staff_")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="transaction")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="transaction_base")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="meria")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="edit_users")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="ant_edit")
                    group_.permissions.add(perms)
            else: group_, created = Group.objects.get_or_create(name="listener")
            group_.save()
            group_meria, created = Group.objects.get_or_create(name="meria")
            if created:
                perms, created = Permission.objects.get_or_create(codename="staff_")
                group_meria.permissions.add(perms)
                perms, created = Permission.objects.get_or_create(codename="meria")
                group_meria.permissions.add(perms)
            group_meria.save()
            
            new_user = User.objects.create(username=username, password=make_password(password))
            new_user.groups.add(group_)

            new_account.id = uuid.uuid4()
            new_account.user = new_user
            new_account.first_name = first_name
            new_account.middle_name = middle_name
            new_account.last_name = last_name
            new_account.user_group = user_group
            new_account.party = party
            new_account.balance = 0
            new_account.save()

            s_write = f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
            f = open("All_users.txt", "a")
            f.write(s_write)
            f.close()

            if form.cleaned_data['save_and_new']:
                return redirect('new-user')
            else:
                return redirect('info-users')
    else:
        type_ = 0
        first_name = "Not stated"
        middle_name = "Not stated"
        last_name = "Not stated"
        user_group = None
        party = 0
        form = accounts.NewAccountFullForm(initial={'type_': type_, 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                                       'id': id, 'user_group': user_group, 'party': party})
    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Добавить новый аккаунт",})

@permission_required('bank.staff_')
@permission_required('bank.edit_users')
def re_new_account_full_add(request, pk):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

    account_ = get_object_or_404(account, id=pk)
    user_ = User.objects.get(id=account_.user.id)
    if request.method == 'POST':
        form = accounts.ReNewAccountForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                tr1 = transaction.objects.filter(creator=account_)
                tr2 = transaction.objects.filter(receiver=account_)
                for i in tr1:
                    if i.counted: i.uncount()
                for i in tr2:
                    if i.counted: i.uncount()
                account_.delete()
                user_.delete()
            else:
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                balance = form.cleaned_data['balance']
                username = translit(form.cleaned_data['username'])
                user_group = form.cleaned_data['user_group']
                party = form.cleaned_data['party']
                
                user_.username = username
                user_.save()

                account_.first_name = first_name
                account_.middle_name = middle_name
                account_.last_name = last_name
                account_.user_group = user_group
                account_.party = party
                account_.balance = balance
                account_.save()
            return redirect('info-users')
    else:
        first_name = account_.first_name
        middle_name = account_.middle_name
        last_name = account_.last_name
        user_group = account_.user_group
        party = account_.party
        balance = account_.balance
        username = user_.username
        form = accounts.ReNewAccountForm(initial={'balance': balance, 'first_name': first_name, 'middle_name': middle_name,
               'last_name': last_name, 'user_group': user_group, 'party': party, 'username': username,})
    return render(request, 'bank/new_and_renew/edit_or_delete.html', {'form': form, 'head': 'Изменение аккаунта'})

@permission_required('bank.staff_')
@permission_required('bank.register')
def update_all_pass(request):
    return render(request, 'bank/accounts/update_all_pass.html')
