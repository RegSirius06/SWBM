from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bank.models import account, transaction, rools
from messenger.models import chat_and_acc

def index(request):
    forbes = account.objects.exclude(party=0).order_by('-balance')[:10]
    antiforbes = account.objects.exclude(party=0).order_by('balance')[:3]
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
    page1 = request.GET.get('page1')
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
            'object_list': items1,
        }
    )

@permission_required('bank.staff_')
def all_accounts_detail_view(request, pk):
    account_ = get_object_or_404(account, id=pk)
    object_list = [i for i in transaction.objects.filter(receiver=account_)]
    for i in transaction.objects.filter(creator=account_):
        object_list.append(i)
    paginator1 = Paginator(object_list, 25)
    page1 = request.GET.get('page1')
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
            'object_list': items1,
        }
    )

@login_required
def my_transaction_view(request):
    acc_all = [i for i in transaction.objects.filter(receiver=request.user.account)]
    for i in transaction.objects.filter(creator=request.user.account):
        acc_all.append(i)
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
        'bank/info_view/my_transactions.html',
        context={
            'object_list': items1,
        }
    )

def rools_view(request):
    return render(
        request,
        'bank/rules/rules.html',
        context={
            'rool_u': rools.objects.filter(num_type='УкТ').order_by('num_pt1', 'num_pt2'),
            'rool_a': rools.objects.filter(num_type='АкТ').order_by('num_pt1', 'num_pt2'),
            'rool_t': rools.objects.filter(num_type='ТкТ').order_by('num_pt1', 'num_pt2'),
            'rool_p': rools.objects.filter(num_type='КпТ').order_by('num_pt1', 'num_pt2'),
        }
    )
