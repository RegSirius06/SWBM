import datetime
import random
import string
import uuid
import json

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

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

class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь:")
    balance = models.FloatField(default=0, verbose_name="Баланс:")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID аккаунта.")#, editable=False)

    first_name = models.CharField(max_length=40, default='Not stated', verbose_name="Имя:")        #   Имя
    middle_name = models.CharField(max_length=40, default='Not stated', verbose_name="Отчество:")  #   Отчество
    last_name = models.CharField(max_length=40, default='Not stated', verbose_name="Фамилия:")     #   Фамилия

    EXISTING_GROUPS = (
        ('None', 'Другое'),
        ('Биология 1', 'Биология 1'),
        ('Биология 2', 'Биология 2'),
        ('Химия 1', 'Химия 1'),
        ('Химия 2', 'Химия 2'),
        ('Информатика', 'Информатика'),
        ('Физика 1', 'Физика 1'),
        ('Физика 2', 'Физика 2'),
        ('Физика 3', 'Физика 3'),
        ('Физика 4', 'Физика 4'),
    )

    user_group = models.CharField(max_length=40, choices=EXISTING_GROUPS, default='None', help_text='Группа обучения', verbose_name="Занятия:")
    party = models.IntegerField(default=0, verbose_name="Отряд:")

    EXISTING_THEMES = (
        ('default', 'По-умолчанию'),
        ('table-primary', 'Голубой'),
        ('table-secondary', 'Серый'),
        ('table-success', 'Зелёный'),
        ('table-danger', 'Красный'),
        ('table-warning', 'Жёлтый'),
        ('table-info', 'Светло-зелёный'),
        ('table-light', 'Светлая'),
        ('table-dark', 'Тёмная'),

        ('p-3 mb-2', 'По-умолчанию (аналог)'),
        ('p-3 mb-2 bg-primary text-white', 'Голубой (аналог)'),
        ('p-3 mb-2 bg-secondary text-white', 'Серый (аналог)'),
        ('p-3 mb-2 bg-success text-white', 'Зелёный (аналог)'),
        ('p-3 mb-2 bg-danger text-white', 'Красный (аналог)'),
        ('p-3 mb-2 bg-warning text-dark', 'Жёлтый (аналог)'),
        ('p-3 mb-2 bg-info text-dark', 'Светло-зелёный (аналог)'),
        ('p-3 mb-2 bg-light text-dark', 'Светлая (аналог)'),
        ('p-3 mb-2 bg-dark text-white', 'Тёмная (аналог)'),

        ('p-3 mb-2 bg-primary bg-gradient text-white', 'Голубой (аналог, градиент)'),
        ('p-3 mb-2 bg-secondary bg-gradient text-white', 'Серый (аналог, градиент)'),
        ('p-3 mb-2 bg-success bg-gradient text-white', 'Зелёный (аналог, градиент)'),
        ('p-3 mb-2 bg-danger bg-gradient text-white', 'Красный (аналог, градиент)'),
        ('p-3 mb-2 bg-warning bg-gradient text-dark', 'Жёлтый (аналог, градиент)'),
        ('p-3 mb-2 bg-info bg-gradient text-dark', 'Светло-зелёный (аналог, градиент)'),
        ('p-3 mb-2 bg-light bg-gradient text-dark', 'Светлая (аналог, градиент)'),
        ('p-3 mb-2 bg-dark bg-gradient text-white', 'Тёмная (аналог, градиент)'),
    )

    theme_self = models.CharField(max_length=50, choices=EXISTING_THEMES, default='default', help_text="Как это выглядит, можно посмотреть ниже.", verbose_name="Тема:")
    account_status = models.CharField(max_length=100, default='', blank=True, verbose_name="Статус:")

    class Meta:
        ordering = ["party", "last_name"]
        permissions = (
            ("staff_", "Принадлежность к персоналу"),
            ("transaction", "Может создавать транзакции"),
            ("transaction_base", "Может совершать переводы"),
            ("register", "Может регистрировать пользователей"),
            ("edit_users", "Может изменять пользователей"),
            ("ant_edit", "Может изменять объявления"),
            ("meria", "Мэрия в банке"),
        )
    
    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])
    
    def get_absolute_url_for_edit(self):
        return reverse('account-edit-n', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
    
    def info(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}: {self.party} отряд, группа {self.user_group}'
    
    def short_name(self):
        return f'{self.last_name} {self.first_name}'
    
    def get_status(self):
        return f'"{self.account_status}"' if self.account_status != '' else 'не установлен'
    
    def get_number_f(self) -> int:
        fb = [i for i in account.objects.exclude(party=0).order_by('-balance', "party", "last_name")]
        for i in range(len(fb)):
            if fb[i].id == self.id: return i + 1
        return 0
    
    def get_number_a(self) -> int:
        fb = [i for i in account.objects.exclude(party=0).order_by('balance', "party", "last_name")]
        for i in range(len(fb)):
            if fb[i].id == self.id: return i + 1
        return 0
    
    def is_ped(self):
        group = self.user.groups.get(name="pedagogue")
        return group is not None

    def get_transactions(self):
        ret = list()
        arr = transaction.objects.all()
        for i in arr:
            if f'{i.receiver}' != f'{self}' and f'{i.creator}' != f'{self}':
                if f'{self.party}' != f'{i.receiver.last_name[-1]}': continue
            ret.append(i)
        return ret if ret != list() else None

    def account_valid(self, x):
        return f'{self.party}'

    def renew_transactions(self):
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if i.counted: continue
            i.count()
            b = True
        return 'Accept!' if b else 'Already accepted'
    
    def undo_transactions(self):
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if not i.counted: continue
            i.uncount()
            b = True
        return 'Accept!' if b else 'Already accepted'
    
    def update_passwords(self):
        def check_user_in_group(user, group_name): return user.groups.filter(name=group_name).exists()
        def gen_pass(length: int) -> str:
            lang = []
            hard_to_read = "l1IioO0"
            for i in string.printable[:62]:
                if i in hard_to_read: continue
                lang.append(i)
            list_ = []
            for u in User.objects.all():
                list_.append(u.password)
            set_list = set(list_)
            while True:
                pas = ""
                for i in range(length):
                    el = random.choice(lang)
                    pas += el
                if pas not in set_list:
                    return pas
        users = User.objects.exclude(username__icontains='admin').order_by('username')
        s_write = '-' * 30 + '\n'
        for u in users:
            len_pass = 12 if check_user_in_group(u, 'pedagogue') else 8
            username = u.username
            password = gen_pass(len_pass)
            s_write += f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
            u.password = make_password(password)
            u.save()
        f = open("All_users.txt", "w")
        f.write(s_write)
        f.close()
        return "Done!"

class transaction(models.Model):
    date = models.DateField(null=True)
    comment = models.CharField(max_length=70, default='Не указано')
    receiver = models.ForeignKey('account', related_name='received_trans', on_delete=models.CASCADE, null=True, verbose_name="Получатель:")
    creator = models.ForeignKey('account', related_name='created_trans', on_delete=models.CASCADE, null=True, verbose_name="Отправитель:")
    history = models.ForeignKey('account', related_name='history_trans', on_delete=models.CASCADE, null=True, verbose_name="Создатель:")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID транзакции.")
    counted = models.BooleanField(default=False, editable=False)

    SIGN_SET = (
        ('+', 'Начислить'),
        ('-', 'Оштрафовать'),
    )

    sign = models.CharField(max_length=1, choices=SIGN_SET, default='+', verbose_name="Тип транзакции:")
    cnt = models.FloatField(default=0, verbose_name="Количество:")
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'От {self.creator} к {self.receiver} на сумму {self.sign}{self.cnt}t (Создал {self.history}): {self.comment}'

    def get_sum(self):
        return f'{self.cnt}t'

    def transaction_valid(self, x):
        return f'{self.receiver.last_name[-1]}'

    def get_absolute_url(self):
        return reverse('transaction-detail', args=[str(self.id)])

    def get_absolute_url_for_edit(self):
        return reverse('transaction-edit', args=[str(self.id)])
    
    def count(self):
        if self.counted: return
        rec = self.receiver
        crt = self.creator
        if self.sign == '+':
            rec.balance = rec.balance + self.cnt
            rec.save()
            crt.balance = crt.balance - self.cnt
            crt.save()
        else:
            rec.balance = rec.balance - self.cnt
            rec.save()
            crt.balance = crt.balance + self.cnt
            crt.save()
        self.counted = True
        self.save()
        return
    
    def uncount(self):
        if not self.counted: return
        rec = self.receiver
        crt = self.creator
        if self.sign == '+':
            rec.balance = rec.balance - self.cnt
            rec.save()
            crt.balance = crt.balance + self.cnt
            crt.save()
        else:
            rec.balance = rec.balance + self.cnt
            rec.save()
            crt.balance = crt.balance - self.cnt
            crt.save()
        self.counted = False
        self.save()
        return

class rools(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    
    EXISTING_TYPES_OF_RULES = (
        ('УкТ', 'Уголовный кодекс'),
        ('АкТ', 'Административный кодекс'),
        ('ТкТ', 'Трудовой кодекс'),
        ('КпТ', 'Кодекс премий'),
    )

    num_type = models.CharField(max_length=3, choices=EXISTING_TYPES_OF_RULES, default='УкТ', verbose_name="Раздел законов:")
    
    num_pt1 = models.IntegerField(default=1, help_text="Раздел кодекса")
    num_pt2 = models.IntegerField(default=0, help_text="Часть раздела")
    comment = models.CharField(max_length=250, default='Не указано')
    punishment = models.CharField(max_length=100, default='Не указано')
    
    class Meta:
        ordering = ["num_type", "num_pt1", "num_pt2"]

    def get_num(self):
        return f'{self.num_type} {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'УкТ {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self):
        return f'УкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'УкТ {self.num_pt1}.{self.num_pt2}'

class good(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    name = models.CharField(max_length=250, default='', verbose_name="Название:")
    comment = models.CharField(max_length=250, default='', verbose_name="Комментарий:")
    cost = models.FloatField(default=0, verbose_name="Цена:")
    
    def __str__(self):
        return f'{self.name} - {self.cost}t'
    
    def get_num(self):
        return f'{self.cost}t'
    
    def get_absolute_url(self):
        return reverse('good-renew', args=[str(self.id)])
    
    class Meta:
        ordering = ["-cost"]

class plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    time = models.CharField(max_length=250, default='', verbose_name="Во сколько:")
    comment = models.CharField(max_length=250, default='', verbose_name="Комментарий:")
    number = models.IntegerField(default=0, verbose_name="Номер в списке: ")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    
    def __str__(self):
        return f'{self.number} - {self.time}; {self.comment}'
    
    def get_absolute_url(self):
        return reverse('plans-renew', args=[str(self.id)])
    
    class Meta:
        ordering = ["number"]

class daily_answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    name = models.TextField(max_length=500, verbose_name='Название задачи:', default='none')
    text = models.TextField(max_length=1000, verbose_name='Условие задачи:')
    cnt = models.FloatField(default=0, verbose_name="Награда:")
    status = models.BooleanField(default=False, verbose_name="Это задача смены?")

    class Meta:
        ordering = ["cnt"]

    def __str__(self):
        return f'{self.name}: на {self.cnt}'
    
    def get_absolute_url(self):
        return reverse('answers-renew', args=[str(self.id)])
