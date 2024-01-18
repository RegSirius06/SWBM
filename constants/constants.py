import datetime

from functools import lru_cache

from utils.localization import get_smth_from_lc, get_const_from_lc, get_error_from_lc

@lru_cache(None)
def get_const_bank_models(request: str) -> any:
    return get_smth_from_lc("bank", "models", '--'.join(request.split(', ')))

@lru_cache(None)
def get_const_bank_forms(request: str) -> any:
    return get_smth_from_lc("bank", "forms", '--'.join(request.split(', ')))

@lru_cache(None)
def get_const_messenger_models(request: str) -> any:
    return get_smth_from_lc("messenger", "models", '--'.join(request.split(', ')))

@lru_cache(None)
def get_const_messenger_forms(request: str) -> any:
    return get_smth_from_lc("messenger", "forms", '--'.join(request.split(', ')))

@lru_cache(None)
def get_error(request: str) -> any:
    return get_error_from_lc(request)

EXISTING_GROUPS = tuple(tuple(x) for x in get_const_from_lc('EXISTING_GROUPS'))

EXISTING_THEMES = tuple(tuple(x) for x in get_const_from_lc('EXISTING_THEMES'))

EXISTING_TYPES_OF_RULES = tuple(tuple(x) for x in get_const_from_lc('EXISTING_TYPES_OF_RULES'))

# Все начисления +, все штрафы -
# ВНИМАНИЕ!!! ЛИЧНЫЙ ПЕРЕВОД ДОЛЖЕНИ ИДТИ СО ЗНАКОМ +
SIGN_SET_ALL = tuple(tuple(x) for x in get_const_from_lc('SIGN_SET_ALL'))
SIGN_SET = tuple(tuple(x) for x in get_const_from_lc('SIGN_SET'))

PERMISSIONS = tuple(tuple(x) for x in get_const_from_lc('PERMISSIONS'))

EXISTING_TYPES = tuple(tuple(x) for x in get_const_from_lc('EXISTING_TYPES'))

__date_of_start__ = dict(get_const_from_lc("DATE_START"))
DATE_START_OF_ = datetime.date(year=__date_of_start__["year"], month=__date_of_start__["month"], day=__date_of_start__["day"])
DATE_END_OF_ = DATE_START_OF_ + datetime.timedelta(days=__date_of_start__["distance"])

PICTURE_TYPES = tuple(tuple(x) for x in get_const_from_lc('PICTURE_TYPES'))

CONFLICT_SOLVES = tuple(tuple(x) for x in get_const_from_lc('CONFLICT_SOLVES'))
