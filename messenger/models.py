import datetime
import os
import uuid
import json

from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.conf import settings

from bank.models import account
from utils import gens, crypto, text
from constants.constants import PICTURE_TYPES, get_const_messenger_models as gc

class ListField(models.TextField):
    description = "Custom list field"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return json.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return ''
        return json.dumps(value)

class EncryptedTextField(models.TextField):
    description = "Custom encrypted text (with dictionary) field"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return {"msg": "", "msg_d": "", "key": "", "alf": ""}
        try: return json.loads(value)
        except: return {"msg": "", "msg_d": "", "key": "", "alf": "BOTH"}
    
    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return {"msg": "", "msg_d": "", "key": "", "alf": ""}
        try: return json.loads(value)
        except json.JSONDecodeError: return eval(value)
    
    def get_prep_value(self, value):
        if value is None:
            return ""
        return json.dumps(value)

class message(models.Model):
    date = models.DateField(default=datetime.date(year=1, month=1, day=1), verbose_name=gc("message, fields, date, verbose_name"))
    time = models.TimeField(default=datetime.time(hour=0), verbose_name=gc("message, fields, time, verbose_name"))
    receiver = models.ForeignKey('chat', blank=True, on_delete=models.CASCADE, null=True,
                                 verbose_name=gc("message, fields, receiver, verbose_name"))
    creator = models.ForeignKey(account, on_delete=models.CASCADE, null=True, verbose_name=gc("message, fields, creator, verbose_name"))
    text = EncryptedTextField(verbose_name=gc("message, fields, text, verbose_name"))
    anonim = models.BooleanField(default=False, verbose_name=gc("message, fields, anonim, verbose_name"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("message, fields, id, help_text"))
    date_of_edit = models.DateField(default=datetime.date(year=1, month=1, day=1),
                                    verbose_name=gc("message, fields, date_of_edit, verbose_name"))
    time_of_edit = models.TimeField(default=datetime.time(hour=0),
                                    verbose_name=gc("message, fields, time_of_edit, verbose_name"))
    editable = models.BooleanField(default=True, editable=False)
    history = models.BooleanField(default=False, editable=False)
    anonim_legacy = models.BooleanField(default=False, editable=False)
    answer_for = models.ForeignKey('message', blank=True, on_delete=models.CASCADE, null=True,
                                   verbose_name=gc("message, fields, answer_for, verbose_name"))

    def get_absolute_url(self):
        x = chat_valid.objects.get(what_chat=self.receiver) if self.receiver is not None else None
        flag = x is not None
        if not flag:
            flag = self.receiver is None
        else: flag = x.avaliable
        return reverse('messages-edit-n', args=[str(self.id)]) if flag else None

    def get_absolute_url_for_detail_view(self):
        return reverse('messages-detail', args=[str(self.id)])

    def get_absolute_url_for_view_answer(self):
        if self.answer_for: return reverse('messages-detail', args=[str(self.answer_for.id)])
        else: return None

    def get_absolute_url_for_resend(self):
        if self.receiver: return reverse('messages-resend', args=[str(self.receiver.id), str(self.id)])
        else: return reverse('messages-resend', args=['global', str(self.id)])

    def get_text_for_view_answer(self):
        def_text = gc("message, methods, get_text_for_view_answer")
        if self.answer_for: return def_text[0] + \
            (f"{self.answer_for.creator}" if not self.answer_for.anonim else def_text[1])
        else: return None
    
    def get_date(self):
        return f'{self.date} {gc("message, methods, get_date")} {self.time}'.split('.')[0]
    
    def anonim_status(self):
        def_text = gc("message, methods, anonim_status")
        return def_text[0] if self.anonim or self.anonim_legacy else def_text[1]

    def __str__(self):
        def_text = gc("message, methods, __str__")
        return f'{self.date}: ' + (def_text[0] if self.receiver is None else f'{def_text[1]} {self.receiver}') + ' ' + \
            (f'{def_text[2]} {self.creator}' if not self.anonim else def_text[3])
    
    def encrypt_data(self, message: str):
        self.text = {"msg": "", "msg_d": "", "key": "", "alf": ""}
        self.text["alf"] = crypto.get_best_alf(message)
        self.text["key"] = gens.key_gen(self.text["alf"])
        self.text["msg"], self.text["msg_d"] = crypto.encode(self.text["key"], self.text["alf"], message)
        try: self.save()
        except: pass
        return self.text
    
    def decrypt_data(self):
        return f'{crypto.decode(self.text["key"], self.text["alf"], self.text["msg"], self.text["msg_d"])}'

    def display_text(self):
        f = self.date == self.date_of_edit and self.time == self.time_of_edit
        add_text = text.get_change_msg(self.date_of_edit, self.time_of_edit) if not f else ''
        return f'{crypto.decode(self.text["key"], self.text["alf"], self.text["msg"], self.text["msg_d"])}' + add_text

    class Meta:
        ordering = ["-date", "-time"]

class chat(models.Model):
    cnt = models.IntegerField(default=1, editable=False)
    name = models.CharField(max_length=50, default='', verbose_name=gc("chat, fields, name, verbose_name"))
    description = models.CharField(max_length=500, default='', verbose_name=gc("chat, fields, description, verbose_name"))
    creator = models.ForeignKey(account, related_name='creator_chat', on_delete=models.CASCADE, null=True,
                                verbose_name=gc("chat, fields, creator, verbose_name"))
    anonim = models.BooleanField(default=False, verbose_name=gc("chat, fields, anonim, verbose_name"))
    anonim_legacy = models.BooleanField(default=False, verbose_name=gc("chat, fields, anonim_legacy, verbose_name"))
    avaliable_resend_messages = models.BooleanField(default=True, verbose_name=gc("chat, fields, avaliable_resend_messages, verbose_name"))
    chat_ico = models.ImageField(verbose_name=gc("chat, fields, chat_ico, verbose_name"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("chat, fields, id, help_text"))

    def __str__(self):
        def_text = gc("chat, methods, __str__")
        return f'{self.name} ({def_text[0]} {self.creator}): {self.cnt} {def_text[1]}'

    def get_absolute_url(self):
        return reverse('chats-n', args=[str(self.id)]) if chat_valid.objects.get(what_chat=self).avaliable else None

    def get_absolute_url_for_edit(self):
        return reverse('chats-edit-n', args=[str(self.id)]) if chat_valid.objects.get(what_chat=self).avaliable else None

    def get_absolute_url_from_archive(self):
        return reverse('chats-archived-n', args=[str(self.id)])

    def get_absolute_url_for_msg(self):
        return reverse('update-messages', args=[str(self.id)])

    def resend_status(self):
        return self.avaliable_resend_messages

    def anonim_status(self):
        def_text = gc("chat, methods, anonim_status")
        return def_text[0] if self.anonim else def_text[1] if self.anonim_legacy else def_text[2]

    def archive(self):
        chat_validator = chat_valid.objects.get(what_chat=self)
        chat_validator.avaliable = False
        list_x = chat_validator.get_all_CAA()
        for i in list_x: i.read_chat()
        chat_validator.save()

    def dearchive(self):
        chat_validator = chat_valid.objects.get(what_chat=self)
        chat_validator.avaliable = True
        list_x = chat_validator.get_all_CAA()
        for i in list_x: i.unread_chat()
        chat_validator.save()

    def get_read_status(self, acc: account):
        CAA = chat_and_acc.objects.filter(what_chat=self).get(what_acc=acc)
        return CAA.readen

    def get_img(self):
        return static(f'messenger/images/{self.chat_ico}')

    def chat_valid(self):
        return f'{self}'

    class Meta:
        ordering = ["name"]

class chat_valid(models.Model):
    what_chat = models.OneToOneField('chat', on_delete=models.CASCADE, null=True,
                                     verbose_name=gc("chat_valid, fields, what_chat, verbose_name"))
    avaliable = models.BooleanField(default=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("chat_valid, fields, id, help_text"))
    list_members = ListField(default=[], null=True, verbose_name=gc("chat_valid, fields, list_members, verbose_name"))
    list_messages = ListField(default=[], null=True, verbose_name=gc("chat_valid, fields, list_messages, verbose_name"))

    def __str__(self):
        def_text = gc("chat_valid, methods, __str__")
        return f'{self.what_chat} ' + (def_text[0] if self.avaliable else def_text[1])
    
    def getting_access(self, acc: account):
        for i in self.list_members:
            if f'{acc.id}' == f'{i}': return True
        return False
    
    def getting_access_id(self, acc: uuid):
        for i in self.list_members:
            if f'{acc}' == f'{i}': return True
        return False
    
    def add_msg(self, msg: message):
        if self.list_messages is None:
            self.list_messages = []
        self.list_messages.append(f'{msg.id}')
        list_x = list(self.get_all_CAA())
        for i in list_x:
            i.readen = False
            i.save()
        self.save()
        return
    
    def get_all_msg(self):
        list_x = [uuid.UUID(i) for i in self.list_messages]
        return message.objects.filter(id__in=list_x)
    
    def get_all_CAA(self):
        return chat_and_acc.objects.filter(what_chat=self.what_chat)

class chat_and_acc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("chat_and_acc, fields, id, help_text"))
    what_chat = models.ForeignKey('chat', on_delete=models.CASCADE, null=True,
                                  verbose_name=gc("chat_and_acc, fields, what_chat, verbose_name"))
    what_acc = models.ForeignKey(account, on_delete=models.CASCADE, null=True,
                                 verbose_name=gc("chat_and_acc, fields, what_acc, verbose_name"))
    readen = models.BooleanField(default=False, editable=False)

    def __str__(self):
        def_text = gc("chat_and_acc, methods, __str__")
        return f'{self.what_chat} ' + ('(' if self.readen else def_text[0]) + f'{def_text[1]} {self.what_acc})'

    def valid_CAA(self):
        return f'{self.what_chat}'

    def read_chat(self):
        self.readen = True
        self.save()
        return
    
    def unread_chat(self):
        self.readen = False
        self.save()
        return

class announcement(models.Model):
    number = models.IntegerField(default=0, verbose_name=gc("announcement, fields, number, verbose_name"))
    creator = models.ForeignKey(account, on_delete=models.CASCADE, null=True,
                                verbose_name=gc("announcement, fields, creator, verbose_name"))
    name = models.TextField(max_length=50, verbose_name=gc("announcement, fields, name, verbose_name"))
    text = models.TextField(max_length=5000, verbose_name=gc("announcement, fields, text, verbose_name"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    status = models.BooleanField(default=False, verbose_name=gc("announcement, fields, status, verbose_name"))
    picture = models.ImageField(verbose_name=gc("announcement, fields, picture, verbose_name"), null=True)
    orientation = models.IntegerField(choices=PICTURE_TYPES, default=0,
                                      verbose_name=gc("announcement, fields, orientation, verbose_name"))

    def get_absolute_url(self):
        return reverse('anns-new-n', args=[str(self.id)])

    def get_img(self):
        return os.path.join(settings.MEDIA_URL, 'announcements', f'{self.picture}')

    def __str__(self):
        return f'{self.name} ({gc("announcement, methods, __str__")} {self.creator})'
    
    class Meta:
        ordering = ["-number"]
