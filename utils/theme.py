from bank.models import account

def get_active_theme(acc: account, delete=False, new=''):
    if delete:
        acc.theme_self = 'default'
        if new != '': acc.theme_self = new
        acc.save()
    return acc.theme_self

def get_type_theme(acc: account) -> str: return 'a' if 'p-3' in acc.theme_self else 'd' if acc.theme_self == 'default' else 't'