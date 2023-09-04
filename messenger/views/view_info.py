import datetime

from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from messenger.models import message, chat, chat_valid, chat_and_acc, announcement
from bank.models import account
from messenger.forms import other
from utils import theme

def index(request):
    anns = announcement.objects.filter(status=True)
    paginator1 = Paginator(anns, 3)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    readen_status = True
    if request.user.is_authenticated:
        for i in list(chat_and_acc.objects.filter(what_acc=request.user.account)):
            readen_status &= i.readen
    return render(
        request,
        'messenger/index.html',
        context={'readen_status': readen_status, 'ant_list': items1,},
    )

@login_required
def list_themes(request):
    date = datetime.date.today()
    time = datetime.time(datetime.datetime.today().hour, datetime.datetime.today().minute, datetime.datetime.today().second,)
    d_t = f'{date} в {time}'
    themes = [i[-1] for i in account.EXISTING_THEMES]
    paginator1 = Paginator(themes, 15)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    if request.method == 'POST':
        form = other.ReNewThemeForm(request.POST, selected=request.user.account.theme_self)
        if form.is_valid():
            x = form.cleaned_data["type_"]
            if x: theme.get_active_theme(request.user.account, delete=True, new=x)
            else: theme.get_active_theme(request.user.account, delete=True)
            return redirect('list-themes')
    else: form = other.ReNewThemeForm(selected=request.user.account.theme_self)
    return render(
        request,
        'messenger/themes/themes.html',
        context={'themes': items1, 'date': d_t, 'form': form, 'theme': theme.get_active_theme(request.user.account),
                 'type': theme.get_type_theme(request.user.account),}
    )

@login_required
def home(request):
    chat_valid_all = list(chat_valid.objects.exclude(avaliable=False))
    list_id_chats = []
    for i in chat_valid_all:
        if i.getting_access(request.user.account):
            list_id_chats.append(i.what_chat.id)
    mess_pr = chat.objects.filter(id__in=list_id_chats)
    chat_and_acc_all = chat_and_acc.objects.filter(what_chat__in=mess_pr).filter(what_acc=request.user.account)
    mess_pub = message.objects.filter(receiver=None)
    paginator1 = Paginator(mess_pr, 25)
    paginator2 = Paginator(mess_pub, 10)
    page1 = request.GET.get('page1')
    page2 = request.GET.get('page2')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    try:
        items2 = paginator2.page(page2)
    except PageNotAnInteger:
        items2 = paginator2.page(1)
    except EmptyPage:
        items2 = paginator2.page(paginator2.num_pages)
    if request.method == 'POST':
        form = other.SetStatus(request.POST)
        if form.is_valid():
            account_ = account.objects.get(id=request.user.account.id)
            new_status = form.cleaned_data['status']
            account_.account_status = new_status
            account_.save()
            return redirect('messages')
    else:
        status = request.user.account.account_status
        form = other.SetStatus(initial={'status': status,})
    context={'items1': items1, 'items2': items2, 'form': form, 'readen_status': chat_and_acc_all,
             'theme': theme.get_active_theme(request.user.account), 'type': theme.get_type_theme(request.user.account),}
    return render(
        request,
        'messenger/home/home.html',
        context=context,
    )
