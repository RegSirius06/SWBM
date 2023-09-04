import uuid
import datetime

from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from messenger.models import message, chat, chat_valid, chat_and_acc
from bank.models import account
from messenger.forms import chats, messages
from utils import theme

@login_required
def new_chat_add(request):
    def make_valid_form(chat_: chat, chat_valid_: chat_valid):
        return f'{chat_valid_.list_members}{chat_.anonim}' if chat_valid_.avaliable else 'None'
    current_user = request.user.account
    if request.method == 'POST':
        form = chats.NewChatForm(request.POST, current_user=current_user)
        if form.is_valid():
            new_message = message()
            new_chat = chat()
            new_chat_valid = chat_valid()

            new_chat.id = uuid.uuid4()
            new_chat.anonim = form.cleaned_data["chat_anonim"]
            new_chat.anonim_legacy = form.cleaned_data["chat_anonim_legacy"]
            new_chat.name = form.cleaned_data["chat_name"]
            new_chat.description = form.cleaned_data["chat_description"]
            members = list(f'{i.id}' for i in form.cleaned_data["chat_members"])
            members.append(f'{request.user.account.id}')
            new_chat.chat_ico = form.cleaned_data["image_choice"]
            new_chat.creator = request.user.account
            new_chat.cnt = len(members)
            
            new_message.id = uuid.uuid4()
            new_message.date = datetime.datetime.today()
            new_message.time = datetime.datetime.now()
            new_message.creator = request.user.account
            new_message.receiver = new_chat
            new_message.text = f'Создан чат {new_chat.name} ({new_chat.description}).'
            new_message.anonim = True
            
            new_chat_valid.id = uuid.uuid4()
            new_chat_valid.what_chat = new_chat
            new_chat_valid.avaliable = True
            new_chat_valid.list_members = members
            new_chat_valid.list_messages.append(f'{new_message.id}')
            members = list(form.cleaned_data["chat_members"])
            members.append(request.user.account)

            set_of_chats_valid = list(chat_valid.objects.filter(avaliable=True))

            new_chat.save()
            new_message.save()
            new_chat_valid.save()

            for acc in members: chat_and_acc.objects.create(id = uuid.uuid4(), what_chat = new_chat, what_acc = acc, readen = False)

            for i in range(len(set_of_chats_valid)):
                if make_valid_form(new_chat, new_chat_valid) == make_valid_form(set_of_chats_valid[i].what_chat, set_of_chats_valid[i]):
                    #return HttpResponse("<h2>Уже сейчас подобный чат существует. Надо только покопаться... не в архиве. <a href=\"/\">Назад...<a/></h2>")
                    return redirect('chats-new-conflict', new_chat.id, new_message.id, new_chat_valid.id, set_of_chats_valid[i].what_chat.id)

            return redirect('messages')
    else:
        form = chats.NewChatForm(current_user=current_user)

    return render(
        request,
        'messenger/new_and_renew/add_new.html',
        {'form': form, 'head': "Создание нового чата",
         'foot': "Нельзя удалять/добавлять новых участников чата."}
    )

@login_required
def new_chat_add_confilct(request, new_chat_id, new_message_id, new_chat_valid_id, existing_chat_id):
    new_chat = chat.objects.get(id=new_chat_id)
    new_message = message.objects.get(id=new_message_id)
    new_chat_valid = chat_valid.objects.get(id=new_chat_valid_id)
    existing_chat = chat.objects.get(id=existing_chat_id)
    existing_chat.archive()
    if request.method == 'POST':
        form = chats.NewChatFormConflict(request.POST)
        if form.is_valid():
            solve = int(form.cleaned_data['solve'])
            
            if solve == 2:
                new_chat_valid.delete()
                new_message.delete()
                new_chat.delete()
                existing_chat.dearchive()
                return redirect('messages')
            
            if solve == 1:
                new_chat_valid.delete()
                new_message.delete()
                new_chat.delete()
                return redirect('messages')

            if solve == 0:
                pass

            return redirect('messages')
    else:
        form = chats.NewChatFormConflict()

    return render(request, 'messenger/chats/chats_new_conflict.html', {'form': form,})

@login_required
def chat_view(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    chat_and_acc_all_ = chat_valid_.get_all_CAA()
    chat_and_acc_ = chat_and_acc_all_.get(what_acc=request.user.account)
    chat_and_acc_.readen = True
    chat_and_acc_.save()
    message_all_ = chat_valid_.get_all_msg()
    paginator1 = Paginator(message_all_, 20)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    len_mess = 2000
    if request.method == 'POST':
        form = messages.NewMessageForm_WithoutAnonim(request.POST) if chat_.anonim or not chat_.anonim_legacy\
                else messages.NewMessageForm(request.POST)
        form2 = chats.SetReadStatusForm(request.POST)
        if form.is_valid():
            if len(list(chat_valid_.list_messages)) >= len_mess:
                redirect('messages')
            message_ = message()
            message_.id = uuid.uuid4()
            message_.date = datetime.datetime.today()
            message_.time = datetime.datetime.today()
            message_.creator = request.user.account
            message_.receiver = chat_
            message_.anonim_legacy = chat_.anonim
            message_.text = form.cleaned_data['message_text']
            if chat_.anonim_legacy: message_.anonim = form.cleaned_data['message_anonim']
            else: message_.anonim = chat_.anonim
            message_.save()
            chat_valid_.add_msg(message_)
            if len(list(chat_valid_.list_messages)) >= len_mess:
                last_message = message()
                last_message.id = uuid.uuid4()
                last_message.date = datetime.datetime.today()
                last_message.time = datetime.datetime.today()
                last_message.creator = chat_.creator
                last_message.receiver = chat_
                last_message.anonim_legacy = chat_.anonim
                last_message.text = f'В чате накопилось 2000 сообщений, поэтому он будет заархивирован.\n\nДля вашего удобства будет создан новый подобный чат.'
                last_message.anonim = True
                last_message.save()
                chat_valid_.add_msg(last_message)
                
                new_message = message()
                new_chat = chat()
                new_chat_valid = chat_valid()

                new_chat.id = uuid.uuid4()
                new_chat.anonim = chat_.anonim
                new_chat.anonim_legacy = chat_.anonim_legacy
                new_chat.name = chat_.name
                new_chat.description = chat_.description
                new_chat.creator = chat_.creator
                new_chat.cnt = chat_.cnt
                
                new_message.id = uuid.uuid4()
                new_message.date = datetime.datetime.today()
                new_message.time = datetime.datetime.now()
                new_message.creator = chat_.creator
                new_message.receiver = new_chat
                new_message.text = f'В предыдущем чате был достигнут лимит по количеству сообщений.\n\nВместо него создан аналогичный чат \"{new_chat.name} ({new_chat.description}).\"'
                new_message.anonim = True
                
                new_chat_valid.id = uuid.uuid4()
                new_chat_valid.what_chat = new_chat
                new_chat_valid.avaliable = True
                new_chat_valid.list_members = list(chat_valid_.list_members)
                new_chat_valid.list_messages = []
                new_chat_valid.list_messages.append(f'{new_message.id}')
                members = list(account.objects.filter(id__in=list(chat_valid_.list_members)))

                new_chat.save()
                new_message.save()
                new_chat_valid.save()
                chat_.archive()
                
                for acc in members: chat_and_acc.objects.create(id = uuid.uuid4(), what_chat = new_chat, what_acc = acc, readen = False)

                return redirect(new_chat.get_absolute_url())
            return redirect(chat_.get_absolute_url())
        if form2.is_valid():
            if chat_and_acc_.readen:
                chat_and_acc_.unread_chat()
                return redirect('messages')
            else:
                chat_and_acc_.read_chat()
            return redirect(chat_.get_absolute_url())
    else:
        form2 = chats.SetReadStatusForm()
        anonim = False
        text = ''
        form = messages.NewMessageForm(initial={'message_text': text, 'message_anonim': anonim,}) \
            if not chat_.anonim and chat_.anonim_legacy else messages.NewMessageForm_WithoutAnonim(initial={'message_text': text})

    return render(
        request,
        'messenger/chats/chats_view_n.html',
        {'form': form, 'chat': chat_, 'items2': items1, 'form2': form2, 'readen_status': chat_and_acc_.readen,
         'theme': theme.get_active_theme(request.user.account), 'type': theme.get_type_theme(request.user.account),}
        )

@login_required
def chat_archived_view(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    #chat_and_acc_all_ = chat_valid_.get_all_CAA()
    message_all_ = chat_valid_.get_all_msg()
    paginator1 = Paginator(message_all_, 220)
    page1 = request.GET.get('page2')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'messenger/chats/chats_archived_view_n.html',
        {'items2': items1, 'chat': chat_,
         'theme': theme.get_active_theme(request.user.account), 'type': theme.get_type_theme(request.user.account),}
    )

@login_required
def chat_archive(request):
    chat_valid_ = chat_valid.objects.exclude(avaliable=True)
    message_all_ = [i.what_chat for i in chat_valid_]
    paginator1 = Paginator(message_all_, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(request, 'messenger/chats/chat_archive.html', {'messages': items1,})

@login_required
def re_new_chat_add(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    if chat_.creator == request.user.account:
        anon_prov = not chat_.anonim and not chat_.anonim_legacy
        current_users = account.objects.filter(id__in=[uuid.UUID(i) for i in chat_valid_.list_members])
        if request.method == 'POST':
            form = chats.ReNewChatFormAnonim(request.POST, current_users=current_users, current_user=request.user.account) if anon_prov\
                    else chats.ReNewChatFormBase(request.POST, current_users=current_users, current_user=request.user.account)
            if form.is_valid():
                chat_.name = form.cleaned_data['chat_name']
                chat_.description = form.cleaned_data['chat_text']
                if anon_prov: chat_.anonim_legacy = form.cleaned_data['chat_anonim']
                creator_chat = form.cleaned_data['chat_creator']
                chat_.chat_ico = form.cleaned_data["image_choice"]
                if creator_chat is not None: chat_.creator = creator_chat
                chat_.save()
                if form.cleaned_data['delete']:
                    chat_.archive()
                    return redirect('messages')
                return redirect(chat_.get_absolute_url())
        else:
            anonim = chat_.anonim_legacy
            name = chat_.name
            text = chat_.description
            chat_ico = chat_.chat_ico
            form = chats.ReNewChatFormAnonim(initial={'chat_text': text, 'chat_name': name, 'chat_anonim': anonim, 'image_choice': chat_ico,},\
                                       current_users=current_users, current_user=request.user.account) if anon_prov else \
                   chats.ReNewChatFormBase(initial={'chat_text': text, 'chat_name': name, 'image_choice': chat_ico,}, current_users=current_users, current_user=request.user.account)

        return render(
            request,
            'messenger/new_and_renew/edit_or_delete.html',
            {'form': form, 'head': f"Изменение чат \"{ chat_.name }\":", 'delete': "Сохранить и заархивировать",
             'foot': "Вы можете заархивировать чат, нажав на соответствующую кнопку. Чат не будет удалён.",}
        )
    else: return HttpResponse("<h2>Я, конечно, всё понимаю, но <em>этого</em> мне не понять...<br/>К сожалению, вы можете редактировать только те чаты, создателем которых вы являетесь.<a href=\"/\">Назад...</a></h2>")
