from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bank.models import account, autotransaction
from bank.forms import autotransactions
from utils import errors

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def all_autotransactions_view(request):
    all_tr = autotransaction.objects.all()
    paginator1 = Paginator(all_tr, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'bank/autotransactions/states.html',
        context={
            'object_list': items1,
        }
    )

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def re_new_autotransaction_add(request, pk):
    autotransaction_ = get_object_or_404(autotransaction, pk=pk)
    if request.method == 'POST':
        form = autotransactions.ReNewAutoTransactionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["delete"]:
                autotransaction_.delete()
            else:
                autotransaction_.history = request.user.account
                autotransaction_.creator = account.objects.get(last_name='Admin')
                autotransaction_.accounts.set(form.cleaned_data['accounts'])
                autotransaction_.cnt = form.cleaned_data['cnt']
                autotransaction_.skip = form.cleaned_data['skip']
                autotransaction_.sign = form.cleaned_data['sign']
                autotransaction_.comment = form.cleaned_data['comment']
                autotransaction_.save()
            return redirect('autotransactions')
    else:
        accounts = [a.id for a in autotransaction_.accounts.all()]
        comment = autotransaction_.comment
        cnt = autotransaction_.cnt
        sign = autotransaction_.sign
        skip = autotransaction_.skip
        form = autotransactions.ReNewAutoTransactionForm(initial={'skip': skip, 'comment': comment, 'cnt': cnt, 
                                                                  'sign': sign, 'accounts': accounts,})

    return render(request, 'bank/new_and_renew/edit_or_delete.html', {'form': form, 'head': "Изменение автотранзакции"})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_autotransaction_add(request):
    if request.method == 'POST':
        form = autotransactions.NewAutoTransactionForm(request.POST)
        if form.is_valid():
            autotransaction_ = autotransaction()
            autotransaction_.history = request.user.account
            autotransaction_.creator = account.objects.get(last_name='Admin')
            autotransaction_.cnt = form.cleaned_data['cnt']
            autotransaction_.skip = form.cleaned_data['skip']
            autotransaction_.sign = form.cleaned_data['sign']
            autotransaction_.comment = form.cleaned_data['comment']
            autotransaction_.save()
            autotransaction_.accounts.set(form.cleaned_data['accounts'])
            #autotransaction_.save()
            return redirect('autotransactions')
    else:
        comment = "Не указано"
        skip = cnt = 0
        form = autotransactions.ReNewAutoTransactionForm(initial={'skip': skip, 'comment': comment, 'cnt': cnt,})

    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Создание автотранзакции"})
