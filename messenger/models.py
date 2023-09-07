import datetime
import os
import uuid
import json

from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.conf import settings

from bank.models import account

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

class message(models.Model):
    date = models.DateField(verbose_name="Дата:")
    time = models.TimeField(default=datetime.time(hour=0), verbose_name="Время:")
    receiver = models.ForeignKey('chat', related_name='received_mess', blank=True, on_delete=models.CASCADE, null=True, verbose_name="Получатель:")
    creator = models.ForeignKey(account, related_name='created_mess', on_delete=models.CASCADE, null=True, verbose_name="Отправитель:")
    text = models.TextField(max_length=2000, verbose_name='Текст:')
    anonim = models.BooleanField(default=False, verbose_name='Если вы хотите отправить это сообщение анонимно, поставьте здесь галочку.')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID сообщения.")
    anonim_legacy = models.BooleanField(default=False, editable=False)

    def get_absolute_url(self):
        x = chat_valid.objects.get(what_chat=self.receiver) if self.receiver is not None else None
        flag = x is not None
        if not flag: 
            flag = self.receiver is None
            print('nok')
        else: flag = x.avaliable
        return reverse('messages-edit-n', args=[str(self.id)]) if flag else None
    
    def get_date(self):
        return f'{self.date} в {self.time}'.split('.')[0]
    
    def anonim_status(self):
        return 'Анонимно' if self.anonim or self.anonim_legacy else 'Публично'

    def __str__(self):
        return f'{self.date}: ' + ('(глобально)' if self.receiver is None else f'К {self.receiver}') + (f' от {self.creator}' if not self.anonim else ' (анонимно)')
    
    class Meta:
        ordering = ["-date", "-time"]

class chat(models.Model):
    cnt = models.IntegerField(default=1, editable=False)
    name = models.CharField(max_length=50, default='', verbose_name='Название чата:')
    description = models.CharField(max_length=500, default='', verbose_name='Описание чата:')
    creator = models.ForeignKey(account, related_name='creator_chat', on_delete=models.CASCADE, null=True, verbose_name="Создатель:")
    anonim = models.BooleanField(default=False, verbose_name='Если вы хотите сделать чат анонимным, поставьте здесь галочку. Этот параметр неизменяем.')
    anonim_legacy = models.BooleanField(default=False, verbose_name='Поставьте галочку, если хотите разрешить участникам отправлять анонимные сообщения.')
    chat_ico = models.ImageField(verbose_name="Иконка чата:", null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID чата.")

    def __str__(self):
        return f'{self.name} (создал {self.creator}): {self.cnt} участников'

    def get_absolute_url(self):
        return reverse('chats-n', args=[str(self.id)]) if chat_valid.objects.get(what_chat=self).avaliable else None

    def get_absolute_url_for_edit(self):
        return reverse('chats-edit-n', args=[str(self.id)]) if chat_valid.objects.get(what_chat=self).avaliable else None

    def get_absolute_url_from_archive(self):
        return reverse('chats-archived-n', args=[str(self.id)])

    def get_absolute_url_for_msg(self):
        return reverse('update-messages', args=[str(self.id)])
    
    def anonim_status(self):
        return 'Анонимный чат' if self.anonim else \
               'Анонимные сообщения разрешены' if self.anonim_legacy\
                else 'Все сообщения публичные'

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
    what_chat = models.OneToOneField('chat', on_delete=models.CASCADE, null=True, verbose_name="Чат:")
    avaliable = models.BooleanField(default=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    list_members = ListField(default=[], null=True, help_text="Список ID участников:")
    list_messages = ListField(default=[], null=True, help_text="Список ID сообщений:")

    def __str__(self):
        return f'{self.what_chat} ' + ('(доступен)' if self.avaliable else '(не доступен)')
    
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    what_chat = models.ForeignKey('chat', on_delete=models.CASCADE, null=True, verbose_name="Чат:")
    what_acc = models.ForeignKey(account, on_delete=models.CASCADE, null=True, verbose_name="Аккаунт:")
    readen = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.what_chat} ' + ('(' if self.readen else '(не ') + f'прочитан {self.what_acc})'

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
    number = models.IntegerField(default=0, verbose_name="Номер в списке:")
    creator = models.ForeignKey(account, on_delete=models.CASCADE, null=True, verbose_name="Отправитель:")
    name = models.TextField(max_length=50, verbose_name='Название:')
    text = models.TextField(max_length=5000, verbose_name='Текст:')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    status = models.BooleanField(default=False, verbose_name="Объявление принято?")
    picture = models.ImageField(verbose_name="Картинка:", null=True)

    PICTURE_TYPES = (
        (0, "Горизонтально"),
        (1, "Вертикально"),
        (2, "Квадрат"),
    )

    orientation = models.IntegerField(choices=PICTURE_TYPES, verbose_name="Ориентация:", default=0)

    def get_absolute_url(self):
        return reverse('anns-new-n', args=[str(self.id)])

    def get_img(self):
        return os.path.join(settings.MEDIA_URL, 'announcements', f'{self.picture}')

    def __str__(self):
        return f'{self.name} (создал {self.creator})'
    
    class Meta:
        ordering = ["-number"]
