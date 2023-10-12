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

EXISTING_TYPES_OF_RULES = (
    ('УкТ', 'Уголовный кодекс'),
    ('АкТ', 'Административный кодекс'),
    ('ТкТ', 'Трудовой кодекс'),
    ('КпТ', 'Кодекс премий'),
)

# Все начисления +, все штрафы -
# ВНИМАНИЕ!!! ЛИЧНЫЙ ПЕРЕВОД ДОЛЖЕНИ ИДТИ СО ЗНАКОМ +
SIGN_SET = (
    ('p2p+', "Личный перевод"),
    ('dining_services+', "Дежурный в столовой"),
    ('activity+', "Активность"),
    ('salary+', "Зарплата"),
    ('fee+', "Гонорар"),
    ('purchase-', "Покупка"),
    ('fine-', "Штраф"),
)

PERMISSIONS = (
    ("staff_", "Принадлежность к персоналу"),
    ("transaction", "Может создавать транзакции"),
    ("transaction_base", "Может совершать переводы"),
    ("register", "Может регистрировать пользователей"),
    ("edit_users", "Может изменять пользователей"),
    ("ant_edit", "Может изменять объявления"),
    ("meria", "Мэрия в банке"),
)
