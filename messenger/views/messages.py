import datetime
import uuid

from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from messenger.models import message, chat_valid, chat
from messenger.forms import messages
from utils import errors

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
        form = messages.NewMessageForm(request.POST, messages=message.objects.filter(receiver=None))
        if form.is_valid():
            new_message = message()
            new_message.id = uuid.uuid4()
            new_message.date = datetime.datetime.today()
            new_message.time = datetime.datetime.now()
            new_message.date_of_edit = datetime.datetime.today()
            new_message.time_of_edit = datetime.datetime.now()
            new_message.creator = request.user.account
            new_message.receiver = None
            answer_for = form.cleaned_data['message_citate']
            if answer_for: new_message.answer_for = message.objects.get(id=uuid.UUID(answer_for))
            else: new_message.answer_for = None
            text = form.cleaned_data['message_text']
            new_message.encrypt_data(text)
            new_message.anonim = form.cleaned_data['message_anonim']
            """if new_message.creator == new_message.receiver:
                return errors.render_error(
                    request, "messenger", "Отправка сообщения себе",
                    "Неужели вы __настолько__ одиноки?..\n\nК сожалению, нельзя себе отправлять сообщения.",
                    [
                        ("messages-new", "Назад"),
                        ('messages', 'Мой профиль'),
                        ('index_of_messenger', 'Домой'),
                        ('index', 'На главную'),
                    ]
                )"""
            new_message.save()
            return redirect('messages')
    else:
        form = messages.NewMessageForm(initial={'message_text': '',}, messages=message.objects.filter(receiver=None))
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
                    elif message_.editable:
                        text = form.cleaned_data['message_text']
                        message_.text = message_.encrypt_data(text)
                        message_.date_of_edit = datetime.datetime.today()
                        message_.time_of_edit = datetime.datetime.today()
                        if anon_prov: message_.anonim = form.cleaned_data['message_anonim']
                        message_.save()
                    return redirect('messages-edit')
            else:
                anonim = message_.anonim
                text = message_.decrypt_data()
                form = messages.ReNewMessageFormAnonim(initial={'message_text': text, 'message_anonim': anonim,}) \
                    if anon_prov else messages.ReNewMessageFormBase(initial={'message_text': text})

            return render(
                request,
                'messenger/new_and_renew/edit_or_delete.html',
                {'form': form, 'head': "Изменение сообщения",
                'foot': "Вы можете удалить сообщение, нажав на соответствующую кнопку. Сообщение без запроса подтверждения будет удалено.\n\nПересланные и системные сообщения изменять нельзя."})
        else:
            return errors.render_error(
                request, "messenger", "Редактирование сообщений",
                "Я, конечно, всё понимаю, но __этого__ мне не понять...\n\nК сожалению, вы можете редактировать только свои сообщения.",
                [
                    ("messages-edit", "Назад"),
                    ('messages', 'Мой профиль'),
                    ('index_of_messenger', 'Домой'),
                    ('index', 'На главную'),
                ]
            )
    else:
        return errors.render_error(
            request, "messenger", "Редактирование сообщений",
            "Чат с данным сообщением заархивирован.",
            [
                ("messages-edit", "Назад"),
                ('messages', 'Мой профиль'),
                ('index_of_messenger', 'Домой'),
                ('index', 'На главную'),
            ]
        )

@login_required
def message_resend(request, chat_id, message_id):
    glb_chat = 'global'
    if chat_id != glb_chat: chat_ = get_object_or_404(chat, pk=chat_id)
    else: chat_ = glb_chat
    message_ = get_object_or_404(message, pk=message_id)
    f = True
    try:
        chat_valid_ = chat_valid.objects.get(what_chat=chat_)
        f = chat_valid_.getting_access(request.user.account)
    except: pass
    if f:
        flag2 = True
        if chat_ != glb_chat: flag2 = chat_.resend_status()
        if flag2:
            if request.method == 'POST':
                form = messages.ResendMessageForm(request.POST, chats=[i.what_chat for i in chat_valid.objects.all()\
                    if i.avaliable and i.getting_access(request.user.account)], chat=chat_ if chat_ != glb_chat else None)
                if form.is_valid():
                    chats = form.cleaned_data['chats']
                    for i in chats:
                        new_message = message_
                        new_message.id = uuid.uuid4()
                        text = new_message.decrypt_data() +\
                            (f"\n\n(Пересланное сообщение от {new_message.creator})" if not new_message.history else '')
                        new_message.history = True
                        new_message.text = new_message.encrypt_data(text)
                        new_message.creator = request.user.account
                        try: new_message.receiver = chat.objects.get(id=uuid.UUID(i))
                        except: new_message.receiver = None
                        new_message.editable = False
                        new_message.date = datetime.date.today()
                        new_message.time = datetime.datetime.now()
                        new_message.save()
                        if i:
                            chat_valid_i = chat_valid.objects.get(what_chat=chat.objects.get(id=uuid.UUID(i)))
                            chat_valid_i.add_msg(new_message)
                            chat_valid_i.save()
                    return redirect('messages')
            else:
                form = messages.ResendMessageForm(chats=[i.what_chat for i in chat_valid.objects.all()\
                    if i.avaliable and i.getting_access(request.user.account)], chat=chat_ if chat_ != glb_chat else None)

            return render(
                request,
                'messenger/messages/resend_message.html',
                {'form': form, 'chats': True if form.fields["chats"].choices else False, 'message': message_,})
        else:
            return errors.render_error(
                request, "messenger", "Пересылка сообщения",
                "Сообщения данного чата нельзя пересылать.",
                [
                    ('messages', 'Мой профиль'),
                    ('index_of_messenger', 'Домой'),
                    ('index', 'На главную'),
                ]
            )
    else:
        return errors.render_error(
            request, "messenger", "Пересылка сообщения",
            "Вы не имеете доступа к чату, из которого пересылаете сообщение. (Как вы вообще сюда попали?)",
            [
                ('messages', 'Мой профиль'),
                ('index_of_messenger', 'Домой'),
                ('index', 'На главную'),
            ]
        )
