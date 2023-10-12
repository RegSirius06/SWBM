import datetime

EXISTING_TYPES = (
    (0, "Пионер"),
    (1, "Педсостав"),
)

SIGN_SET = (
    ('dining_services+', "Дежурный в столовой"),
    ('activity+', "Активность"),
    ('salary+', "Зарплата"),
    ('fee+', "Гонорар"),
    ('purchase-', "Покупка"),
    ('fine-', "Штраф"),
)

SIGN_SET_ALL = (
    ('p2p+', "Личный перевод"),
    ('dining_services+', "Дежурный в столовой"),
    ('activity+', "Активность"),
    ('salary+', "Зарплата"),
    ('fee+', "Гонорар"),
    ('purchase-', "Покупка"),
    ('fine-', "Штраф"),
)

DATE_START_OF_ = datetime.date(year=2024, month=6, day=25)
DATE_END_OF_ = datetime.date(year=2024, month=6, day=25) + datetime.timedelta(weeks=3)
