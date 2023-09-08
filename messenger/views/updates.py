from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from messenger.models import message, chat, chat_valid, chat_and_acc
from utils import theme

def update_msgs(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    message_all_ = chat_valid_.get_all_msg()
    paginator1 = Paginator(message_all_, 20)
    page1 = request.GET.get('page2')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)

    html = render_to_string(
        'messenger/updates/update_messages.html',
        {'items2': items1, 'theme': theme.get_active_theme(request.user.account), 'type': theme.get_type_theme(request.user.account)}
    )
    return JsonResponse({'html': html,})

def update_chats(request):
    chat_valid_all = list(chat_valid.objects.exclude(avaliable=False))
    list_id_chats = []
    for i in chat_valid_all:
        if i.getting_access(request.user.account):
            list_id_chats.append(i.what_chat.id)
    mess_pr = chat.objects.filter(id__in=list_id_chats)
    chat_and_acc_all = chat_and_acc.objects.filter(what_chat__in=mess_pr).filter(what_acc=request.user.account)
    paginator1 = Paginator(mess_pr, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)

    html = render_to_string('messenger/updates/update_chats.html', {'items1': items1, 'readen_status': chat_and_acc_all})
    return JsonResponse({'html': html})

def update_globals(request):
    mess_pub = message.objects.filter(receiver=None)
    paginator2 = Paginator(mess_pub, 10)
    page2 = request.GET.get('page2')
    try:
        items2 = paginator2.page(page2)
    except PageNotAnInteger:
        items2 = paginator2.page(1)
    except EmptyPage:
        items2 = paginator2.page(paginator2.num_pages)

    html = render_to_string(
        'messenger/updates/update_globals.html',
        {'items2': items2, 'theme': theme.get_active_theme(request.user.account),
         'type': theme.get_type_theme(request.user.account)}
    )
    return JsonResponse({'html': html})
