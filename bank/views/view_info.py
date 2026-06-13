from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bank.models import account, transaction, rules
from messenger.models import chat_and_acc

def index(request):
    forbes = account.objects.exclude(party=0).order_by('-balance')[:10]
    antiforbes = account.objects.exclude(party=0).filter(balance__lt=0).order_by('balance')
    admin = account.objects.get(last_name="Admin")
    for i in antiforbes:
        if i in forbes:
            antiforbes = forbes = None
            break
    readen_status = True
    if request.user.is_authenticated:
        for i in list(chat_and_acc.objects.filter(what_acc=request.user.account)):
            readen_status &= i.readen
    return render(
        request,
        'bank/index.html',
        context={'forbes': forbes, 'antiforbes': antiforbes, 'admin': admin, 'readen_status': readen_status,},
    )

@permission_required('bank.staff_')
def all_accounts_list_view(request):
    acc_all = account.objects.exclude(party=0).order_by('party', 'last_name') #.filter(name=self.request.user.account.balance)
    paginator1 = Paginator(acc_all, 25)
    page1 = request.GET.get('page')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'bank/info_view/balances.html',
        context={
            'is_paginated': paginator1.num_pages > 1,
            'page_obj': items1,
        }
    )

@permission_required('bank.staff_')
def all_accounts_detail_view(request, pk):
    try:
        is_ped = request.user.account.is_ped()
    except AttributeError:
        is_ped = False
    account_ = get_object_or_404(account, id=pk)
    object_list = [i for i in transaction.objects.filter(receiver=account_)]
    for i in transaction.objects.filter(creator=account_):
        object_list.append(i)
    paginator1 = Paginator(object_list, 25)
    page1 = request.GET.get('page')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'bank/info_view/transactions_detail.html',
        context={
            'account': account_,
            'is_paginated': paginator1.num_pages > 1,
            'page_obj': items1,
            'is_ped': is_ped,
        }
    )

@login_required
def my_transaction_view(request):
    acc_all = [i for i in transaction.objects.filter(receiver=request.user.account)]
    for i in transaction.objects.filter(creator=request.user.account):
        acc_all.append(i)
    paginator1 = Paginator(acc_all, 25)
    page1 = request.GET.get('page')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'bank/info_view/my_transactions.html',
        context={
            "is_paginated": paginator1.num_pages > 1,
            'page_obj': items1,
        }
    )

def rules_view(request):
    try:
        is_ped = request.user.account.is_ped()
    except AttributeError:
        is_ped = False
    return render(
        request,
        'bank/rules/rules.html',
        context={
            'rool_u': rules.objects.filter(num_type='УК ЛЕС').order_by('num_pt'),
            'rool_a': rules.objects.filter(num_type='АК ЛЕС').order_by('num_pt'),
            'rool_t': rules.objects.filter(num_type='ТК ЛЕС').order_by('num_pt'),
            'rool_p': rules.objects.filter(num_type='КП ЛЕС').order_by('num_pt'),
            'rool_s': rules.objects.filter(num_type='КС ЛЕС').order_by('num_pt'),
            'is_ped': is_ped
        }
    )
