import uuid
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bank.models import account, transaction, good
from bank.forms import transactions
from utils import errors

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def all_transactions_view(request):
    all_tr = transaction.objects.all()
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
        'bank/transactions/transaction_status.html',
        context={
            'object_list': items1,
        }
    )

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_staff_add(request):
    if request.method == 'POST':
        form = transactions.NewTransactionStaffForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['transaction_receiver']
            for i in [*receiver]:
                new_transaction = transaction()
                new_transaction.id = uuid.uuid4()
                new_transaction.date = form.cleaned_data['transaction_date']
                new_transaction.comment = form.cleaned_data['transaction_comment']
                new_transaction.creator = account.objects.get(last_name='Admin')
                new_transaction.receiver = i
                new_transaction.sign = form.cleaned_data['transaction_sign']
                new_transaction.history = request.user.account
                if new_transaction.creator == new_transaction.receiver:
                    return errors.render_error(
                        request, "bank", "Создание транзакции",
                        "Вы не можете перевести деньги на свой счёт.",
                        [
                            ("new-transaction-staff", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                new_transaction.cnt = form.cleaned_data['transaction_cnt']
                new_transaction.save()
                new_transaction.count()
            return redirect('info-staff')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        form = transactions.NewTransactionStaffForm(initial={'transaction_date': transaction_date, 
                                                             'transaction_comment': transaction_comment,
                                                             'transaction_cnt': transaction_cnt})

    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Добавить новую транзакцию (штраф/премию)"})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_staff_party_add(request):
    if request.method == 'POST':
        form = transactions.NewTransactionStaffFormParty(request.POST)
        if form.is_valid():
            receiver = int(form.cleaned_data['transaction_receiver'])
            all_receivers = account.objects.filter(party=receiver)
            for i in all_receivers:
                new_transaction = transaction()
                new_transaction.id = uuid.uuid4()
                new_transaction.date = form.cleaned_data['transaction_date']
                new_transaction.comment = form.cleaned_data['transaction_comment']
                new_transaction.creator = account.objects.get(last_name='Admin')
                new_transaction.receiver = i
                new_transaction.sign = form.cleaned_data['transaction_sign']
                new_transaction.history = request.user.account
                new_transaction.cnt = form.cleaned_data['transaction_cnt']
                new_transaction.save()
                new_transaction.count()
            return redirect('info-staff')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        form = transactions.NewTransactionStaffFormParty(initial={'transaction_date': transaction_date, 
                                                                  'transaction_comment': transaction_comment, 
                                                                  'transaction_cnt': transaction_cnt})

    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Добавить новую транзакцию (штраф/премию) на отряд"})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_full_add(request):
    not_list_accounts = list(account.objects.filter(party=0).exclude(last_name='Admin'))
    list_accounts = []
    for i in not_list_accounts:
        list_accounts.append(i.id)
    if request.method == 'POST':
        form = transactions.NewTransactionFullForm(request.POST, current_users=list_accounts)
        if form.is_valid():
            receiver = form.cleaned_data['transaction_receiver']
            for i in [*receiver]:
                new_transaction = transaction()
                new_transaction.id = uuid.uuid4()
                new_transaction.date = form.cleaned_data['transaction_date']
                new_transaction.comment = form.cleaned_data['transaction_comment']
                new_transaction.creator = form.cleaned_data['transaction_creator']
                new_transaction.history = form.cleaned_data['transaction_history']
                new_transaction.receiver = i
                new_transaction.sign = form.cleaned_data['transaction_sign']
                if new_transaction.creator == new_transaction.receiver:
                    return errors.render_error(
                        request, "bank", "Создание транзакции",
                        "Неужели вы __настолько__ жадина?",
                        [
                            ("new-transaction-full", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                elif account.objects.get(last_name='Admin') == new_transaction.receiver:
                    return errors.render_error(
                        request, "bank", "Создание транзакции",
                        "Вы не можете перевести деньги на банковский счёт. Сегодня без донатов.",
                        [
                            ("new-transaction-full", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                new_transaction.cnt = form.cleaned_data['transaction_cnt']
                new_transaction.save()
                new_transaction.count()
            return redirect('info-staff')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        form = transactions.NewTransactionFullForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
               'transaction_cnt': transaction_cnt}, current_users=list_accounts,)

    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Добавить новую транзакцию",})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_buy_add(request):
    if request.method == 'POST':
        form = transactions.NewTransactionBuyForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['transaction_receiver']
            for i in [receiver]:
                new_transaction = transaction()
                new_transaction.id = uuid.uuid4()
                new_transaction.date = datetime.datetime.today()
                new_transaction.creator = account.objects.get(last_name='Admin')
                new_transaction.receiver = i
                new_transaction.sign = "purchase-"
                good_dict = form.clean_goods()[0]
                good_list_id = form.clean_goods()[1]
                goods = good.objects.filter(id__in=good_list_id).order_by("-cost")
                cnt = 0
                flag = False
                comment = "Чек за покупку: "
                for gd in goods:
                    cnt += gd.cost * good_dict[gd]
                    comment += f"{gd.name}, {good_dict[gd]} раз: {gd.cost * good_dict[gd]}t; "
                    if cnt > new_transaction.receiver.balance: flag = True
                if flag:
                    return errors.render_error(
                        request, "bank", "Создание чека",
                        f"На покупку не хватает денег.\n\n{comment}\n\nЕсть {new_transaction.receiver.balance}t, а надо {cnt}t.",
                        [
                            ("new-transaction-buy", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                new_transaction.cnt = cnt
                new_transaction.history = request.user.account
                new_transaction.comment = comment
                new_transaction.save()
                new_transaction.count()
            return redirect('info-staff')
    else:
        form = transactions.NewTransactionBuyForm(initial={})

    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Оформить покупку"})

@permission_required('bank.transaction_base')
def new_transaction_base_add(request):
    if request.method == 'POST':
        form = transactions.NewTransactionBaseForm(request.POST)
        if form.is_valid():
            receiver = [form.cleaned_data['transaction_receiver']]
            for i in [receiver]:
                new_transaction = transaction()
                new_transaction.id = uuid.uuid4()
                new_transaction.date = datetime.datetime.today()
                new_transaction.sign = "p2p+"
                new_transaction.comment = form.cleaned_data['transaction_comment']
                new_transaction.creator = request.user.account
                new_transaction.receiver = i
                new_transaction.history = request.user.account
                if new_transaction.creator == new_transaction.receiver:
                    return errors.render_error(
                        request, "bank", "Создание перевода",
                        "Неужели вы __настолько__ жадина?",
                        [
                            ("new-transaction-base", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                elif account.objects.get(last_name='Admin') == new_transaction.receiver:
                    return errors.render_error(
                        request, "bank", "Создание перевода",
                        "Вы не можете перевести деньги на банковский счёт. Сегодня без донатов.",
                        [
                            ("new-transaction-base", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                new_transaction.cnt = form.cleaned_data['transaction_cnt']
                if new_transaction.cnt > request.user.account.balance:
                    return errors.render_error(
                        request, "bank", "Создание перевода",
                        "Вы не можете перевести денег больше, чем у вас есть, хотя вы и гений.",
                        [
                            ("new-transaction-base", "Назад"),
                            ('my-transactions', 'Мой счёт'),
                            ('index_of_bank', 'Домой'),
                            ('index', 'На главную'),
                        ]
                    )
                new_transaction.save()
                new_transaction.count()
            return redirect('my-transactions')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        form = transactions.NewTransactionBaseForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment, 'transaction_cnt': transaction_cnt})

    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'head': "Добавить перевод"})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def re_new_transaction_add(request, pk):
    transaction_ = get_object_or_404(transaction, pk=pk)
    if request.method == 'POST':
        form = transactions.ReNewTransactionStaffForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["delete"]:
                if transaction_.counted: transaction_.uncount()
                transaction_.delete()
            elif form.cleaned_data["edit"]:
                if transaction_.counted: transaction_.uncount()
                else: transaction_.count()
            else:
                transaction_.uncount()
                transaction_.date = form.cleaned_data['transaction_date']
                transaction_.comment = form.cleaned_data['transaction_comment']
                transaction_.sign = form.cleaned_data['transaction_sign']
                transaction_.cnt = form.cleaned_data['transaction_cnt']
                transaction_.history = form.cleaned_data['transaction_history']
                transaction_.save()
                transaction_.count()
            return redirect('info-staff')
    else:
        transaction_history = transaction_.history
        transaction_date = transaction_.date
        transaction_comment = transaction_.comment
        transaction_cnt = transaction_.cnt
        transaction_sign = transaction_.sign
        form = transactions.ReNewTransactionStaffForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
               'transaction_cnt': transaction_cnt, 'transaction_sign': transaction_sign, 'transaction_history': transaction_history,})

    return render(request, 'bank/transactions/transaction_edit_form.html', {'form': form, 'counted': transaction_.counted,})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def renew_transaction(request):
    return render(request, 'bank/transactions/transaction_do.html')

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def undo_transaction(request):
    return render(request, 'bank/transactions/transaction_undo.html')
