import json
import os

from django.conf import settings

info_all = dict()

try:
    with open(os.path.join(settings.BASE_DIR, 'constants', settings.LOCALIZATION_FILE_NAME), 'r', encoding="utf-8") as f:
        info_all = json.load(f)
    print('Localization file was successfully readen from default location!')
except:
    with open(os.path.join(settings.LOCALIZATION_FILE_DIR, settings.LOCALIZATION_FILE_NAME), 'r', encoding="utf-8") as f:
        info_all = json.load(f)
    print('Localization file was successfully readen from settings locatoin!')

#print(info_all)

def __request_handler__(request: str, info: any) -> any:
    rq = request.split('--')
    for i in rq: info = info[i]
    return info

def get_smth_from_lc(type_app: str, type_module: str, request: str) -> any:
    global info_all
    sbj = info_all[type_app][type_module]
    return __request_handler__(request, sbj)

def get_const_from_lc(request: str) -> any:
    global info_all
    sbj = info_all["constants"]
    return __request_handler__(request, sbj)

def get_error_from_lc(request: str) -> any:
    global info_all
    sbj = info_all["errors"]
    return __request_handler__(request, sbj)