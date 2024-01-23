import uuid
import json

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from utils.passwords import gen_pass
from constants.constants import EXISTING_GROUPS, EXISTING_THEMES, EXISTING_TYPES_OF_RULES, PERMISSIONS, SIGN_SET_ALL, get_const_bank_models as gc

class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=gc('account, fields, user, verbose_name'))
    balance = models.FloatField(default=0, verbose_name=gc('account, fields, balance, verbose_name'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc('account, fields, id, help_text'))#, editable=False)

    first_name = models.CharField(max_length=40, default=gc('account, fields, first_name, default'),
                                  verbose_name=gc('account, fields, first_name, verbose_name'))   #   Имя
    middle_name = models.CharField(max_length=40, default=gc('account, fields, middle_name, default'),
                                   verbose_name=gc('account, fields, middle_name, verbose_name')) #   Отчество
    last_name = models.CharField(max_length=40, default=gc('account, fields, last_name, default'),
                                 verbose_name=gc('account, fields, last_name, verbose_name'))     #   Фамилия

    user_group = models.CharField(max_length=40, choices=EXISTING_GROUPS, default='None',
                                  help_text=gc('account, fields, user_group, help_text'),
                                  verbose_name=gc('account, fields, user_group, verbose_name'))
    party = models.IntegerField(default=0, verbose_name=gc('account, fields, party, verbose_name'))

    theme_self = models.CharField(max_length=50, choices=EXISTING_THEMES, default='default',
                                  help_text=gc('account, fields, theme_self, help_text'),
                                  verbose_name=gc('account, fields, theme_self, verbose_name'))
    account_status = models.CharField(max_length=100, default='', blank=True,
                                      verbose_name=gc('account, fields, account_status, verbose_name'))

    class Meta:
        ordering = ["party", "last_name"]
        permissions = PERMISSIONS
    
    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])
    
    def get_absolute_url_for_edit(self):
        return reverse('account-edit-n', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
    
    def info(self) -> str:
        return f'{self.last_name}, {self.first_name} {self.middle_name}: {self.party} {gc("account, methods, info")} {self.user_group}'
    
    def short_name(self) -> str:
        return f'{self.last_name} {self.first_name}'
    
    def get_status(self) -> str:
        return f'"{self.account_status}"' if self.account_status != '' else gc("account, methods, get_status")
    
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
    
    def is_ped(self) -> bool:
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

    def account_valid(self) -> str:
        return f'{self.party}'

    def renew_transactions(self) -> str:
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if i.counted: continue
            i.count()
            b = True
        return 'Accept!' if b else 'Already accepted'
    
    def undo_transactions(self) -> str:
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if not i.counted: continue
            i.uncount()
            b = True
        return 'Accept!' if b else 'Already accepted'
    
    def update_passwords(self) -> str:
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
    date = models.DateField(null=True, verbose_name=gc("transaction, fields, date, verbose_name"))
    comment = models.CharField(max_length=70, default=gc("transaction, fields, comment, default"),
                               verbose_name=gc("transaction, fields, comment, verbose_name"))
    receiver = models.ForeignKey('account', related_name='received_trans', on_delete=models.CASCADE, null=True,
                                 verbose_name=gc("transaction, fields, receiver, verbose_name"))
    creator = models.ForeignKey('account', related_name='created_trans', on_delete=models.CASCADE, null=True,
                                verbose_name=gc("transaction, fields, creator, verbose_name"))
    history = models.ForeignKey('account', related_name='history_trans', on_delete=models.CASCADE, null=True,
                                verbose_name=gc("transaction, fields, history, verbose_name"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("transaction, fields, id, help_text"))
    counted = models.BooleanField(default=False, editable=False)
    sign = models.CharField(max_length=20, choices=SIGN_SET_ALL, default='p2p+',
                            verbose_name=gc("transaction, fields, sign, verbose_name"))
    cnt = models.FloatField(default=0, verbose_name=gc("transaction, fields, cnt, verbose_name"))
    
    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        x = gc("transaction, methods, __str__")
        return f'{x[0]} {self.creator} {x[1]} {self.receiver} {x[2]} {self.cnt}t ({x[3]} {self.history}): {dict(SIGN_SET_ALL)[self.sign]}'

    def get_sum(self) -> str:
        return f'{self.cnt}t'

    def get_type_of(self) -> str:
        return f'{dict(SIGN_SET_ALL)[self.sign]}'

    def transaction_valid(self) -> str:
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
    num_type = models.CharField(max_length=3, choices=EXISTING_TYPES_OF_RULES, default=EXISTING_TYPES_OF_RULES[0][0],
                                verbose_name=gc("rools, fields, num_type, verbose_name"))
    num_pt1 = models.IntegerField(default=1, help_text=gc("rools, fields, num_pt1, help_text"),
                                  verbose_name=gc("rools, fields, num_pt1, verbose_name"))
    num_pt2 = models.IntegerField(default=0, help_text=gc("rools, fields, num_pt2, help_text"),
                                  verbose_name=gc("rools, fields, num_pt2, verbose_name"))
    comment = models.CharField(max_length=250, default=gc("rools, fields, comment, default"),
                               verbose_name=gc("rools, fields, comment, verbose_name"))
    punishment = models.CharField(max_length=100, default=gc("rools, fields, punishment, default"),
                                  verbose_name=gc("rools, fields, punishment, verbose_name"))

    class Meta:
        ordering = ["num_type", "num_pt1", "num_pt2"]

    def get_num(self) -> str:
        return f'{self.num_type} {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else\
            f'{self.num_type} {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self) -> str:
        return f'{self.num_type} {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else\
            f'{self.num_type} {self.num_pt1}.{self.num_pt2}'

class good(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("good, fields, id, help_text"))
    name = models.CharField(max_length=250, default='', verbose_name=gc("good, fields, name, verbose_name"))
    comment = models.CharField(max_length=250, default='', verbose_name=gc("good, fields, comment, verbose_name"))
    cost = models.FloatField(default=0, verbose_name=gc("good, fields, cost, verbose_name"))

    def __str__(self):
        return f'{self.name} - {self.cost}t'
    
    def get_num(self):
        return f'{self.cost}t'
    
    def get_absolute_url(self):
        return reverse('good-renew', args=[str(self.id)])
    
    class Meta:
        ordering = ["-cost"]

class plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("plan, fields, id, help_text"))
    time = models.CharField(max_length=250, default='', verbose_name=gc("plan, fields, time, verbose_name"))
    comment = models.CharField(max_length=250, default='', verbose_name=gc("plan, fields, comment, verbose_name"))
    number = models.IntegerField(default=0, verbose_name=gc("plan, fields, number, verbose_name"))
    
    def __str__(self) -> str:
        return f'{self.number} - {self.time}; {self.comment}'
    
    def get_absolute_url(self):
        return reverse('plans-renew', args=[str(self.id)])
    
    class Meta:
        ordering = ["number"]

class daily_answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=gc("daily_answer, fields, id, help_text"))
    name = models.TextField(max_length=500, verbose_name=gc("daily_answer, fields, name, verbose_name"),
                            default=gc("daily_answer, fields, name, default"))
    text = models.TextField(max_length=1000, verbose_name=gc("daily_answer, fields, text, verbose_name"))
    cnt = models.FloatField(default=0, verbose_name=gc("daily_answer, fields, cnt, verbose_name"))
    status = models.BooleanField(default=False, verbose_name=gc("daily_answer, fields, status, verbose_name"))

    class Meta:
        ordering = ["cnt"]

    def __str__(self) -> str:
        return f'{self.name}: {gc("daily_answer, methods, __str__")} {self.cnt}'
    
    def get_absolute_url(self):
        return reverse('answers-renew', args=[str(self.id)])
