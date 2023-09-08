import datetime
import uuid

from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from messenger.models import message, chat_valid
from messenger.forms import messages

@login_required
def home_send(request):
    mess_pr = message.objects.filter(creator=request.user.account).exclude(receiver=None)
    mess_pr_ = message.objects.filter(creator=request.user.account).exclude(receiver=None)
    if list(mess_pr) != []:
        i = 0
        while True:
            if not chat_valid.objects.get(what_chat=mess_pr[i].receiver).avaliable:
                mess_pr = mess_pr.exclude(id=mess_pr[i].id)
                i -= 1
            i += 1
            if i >= len(mess_pr): break
    if list(mess_pr_) != []:
        i = 0
        while True:
            if chat_valid.objects.get(what_chat=mess_pr_[i].receiver).avaliable:
                mess_pr_ = mess_pr_.exclude(id=mess_pr_[i].id)
                i -= 1
            i += 1
            if i >= len(mess_pr_): break
    mess_pub = message.objects.filter(creator=request.user.account).filter(receiver=None)
    paginator1 = Paginator(mess_pr, 25)
    paginator2 = Paginator(mess_pub, 25)
    paginator3 = Paginator(mess_pr_, 25)
    page1 = request.GET.get('page1')
    page2 = request.GET.get('page2')
    page3 = request.GET.get('page3')
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
    try:
        items3 = paginator3.page(page3)
    except PageNotAnInteger:
        items3 = paginator3.page(1)
    except EmptyPage:
        items3 = paginator3.page(paginator3.num_pages)
    return render(
        request,
        'messenger/messages/messages_list.html',
        context={'messages': items1, 'messages_public': items2, 'items3': items3,},
    )

@login_required
def new_message_add(request):
    if request.method == 'POST':
        form = messages.NewMessageForm(request.POST)
        if form.is_valid():
            new_message = message()
            new_message.id = uuid.uuid4()
            new_message.date = datetime.datetime.today()
            new_message.time = datetime.datetime.now()
            new_message.creator = request.user.account
            new_message.receiver = None
            text = form.cleaned_data['message_text']
            new_message.encrypt_data(text)
            new_message.anonim = form.cleaned_data['message_anonim']
            #if new_message.creator == new_message.receiver:
            #    return HttpResponse("<h2>Неужели вы <em>настолько</em> одиноки?..<br/>К сожалению, нельзя себе отправлять сообщения.<a href=\"/\">Назад...</a></h2>")
            new_message.save()
            return redirect('messages')
    else:
        form = messages.NewMessageForm(initial={'message_text': '',})

    return render(
        request,
        'messenger/new_and_renew/add_new.html',
        {'form': form, 'head': "Отправить новое глобальное сообщение", 'name': "Отправить",
         'foot': "Анонимное сообщение можно сделать неанонимным, неанонимное сообщение нельзя сделать анонимным.",}
    )

@login_required
def re_new_message_add(request, pk):
    message_ = get_object_or_404(message, pk=pk)
    x = chat_valid.objects.get(what_chat=message_.receiver) if message_.receiver is not None else None
    flag = x is not None
    if not flag: flag = message_.receiver is None
    else: flag = x.avaliable
    if flag:
        if message_.creator == request.user.account:
            anon_prov = message_.anonim and not message_.anonim_legacy

            if request.method == 'POST':
                form = messages.ReNewMessageFormAnonim(request.POST) if anon_prov\
                        else messages.ReNewMessageFormBase(request.POST)
                if form.is_valid():
                    if form.cleaned_data['delete']:
                        if message_.receiver is not None:
                            chat_valid_ = chat_valid.objects.get(what_chat=message_.receiver)
                            for i in range(len(chat_valid_.list_messages)):
                                if f'{chat_valid_.list_messages[i]}' == f'{message_.id}':
                                    del chat_valid_.list_messages[i]
                                    break
                        message_.delete()
                    else:
                        text = form.cleaned_data['message_text'] + f"\n\n(Изменено {datetime.date.today()} в {datetime.time(hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, second=datetime.datetime.now().second)})"
                        message_.encrypt_data(text)
                        if anon_prov: message_.anonim = form.cleaned_data['message_anonim']
                        message_.save()
                    return redirect('messages-edit')
            else:
                anonim = message_.anonim
                text = message_.decrypt_data()
                text = text[:-34] if text[-1] == ')' and "\n\n(Изменено " in text else text
                form = messages.ReNewMessageFormAnonim(initial={'message_text': text, 'message_anonim': anonim,}) \
                    if anon_prov else messages.ReNewMessageFormBase(initial={'message_text': text})

            return render(
                request,
                'messenger/new_and_renew/edit_or_delete.html',
                {'form': form, 'head': "Изменение сообщения",
                 'foot': "Вы можете удалить сообщение, нажав на соответствующую кнопку. Сообщение без запроса подтверждения будет удалено."})
        else: return HttpResponse("<h2>Я, конечно, всё понимаю, но <em>этого</em> мне не понять...<br/>К сожалению, вы можете редактировать только свои сообщения. <a href=\"/\">Назад...</a></h2>")
    else: return HttpResponse("<h2>Чат с данным сообщением заархивирован. <a href=\"/\">Назад...<a/></h2>")
