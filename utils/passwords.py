import string
import random

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

def is_valid_password(password):
    try:
        validate_password(password)
    except Exception as e:
        return e
    return True

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
