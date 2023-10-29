import uuid
import json

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from utils.passwords import gen_pass
from constants.bank.models import EXISTING_GROUPS, EXISTING_THEMES, EXISTING_TYPES_OF_RULES, PERMISSIONS, SIGN_SET

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

    user_group = models.CharField(max_length=40, choices=EXISTING_GROUPS, default='None', help_text='Группа обучения', verbose_name="Занятия:")
    party = models.IntegerField(default=0, verbose_name="Отряд:")

    theme_self = models.CharField(max_length=50, choices=EXISTING_THEMES, default='default', help_text="Как это выглядит, можно посмотреть ниже.", verbose_name="Тема:")
    account_status = models.CharField(max_length=100, default='', blank=True, verbose_name="Статус:")

    class Meta:
        ordering = ["party", "last_name"]
        permissions = PERMISSIONS
    
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
    sign = models.CharField(max_length=20, choices=SIGN_SET, default='p2p+', verbose_name="Тип транзакции:")
    cnt = models.FloatField(default=0, verbose_name="Количество:")
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'От {self.creator} к {self.receiver} на сумму {self.cnt}t (Создал {self.history}): {dict(SIGN_SET)[self.sign]}'

    def get_sum(self):
        return f'{self.cnt}t'

    def get_type_of(self):
        return f'{dict(SIGN_SET)[self.sign]}'

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
        if '+' in self.sign:
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
        if '+' in self.sign:
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
