import telebot
import sqlite3
import json

from telebot import types
from django.db.models import Q
from django.contrib.auth.models import User
from bank.models import account, transaction, plan, rools, daily_answer, good
from server.server import get_link4bot

def get_acc(user_id):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auth_user WHERE telegramm_id = ?", (user_id,))
        user = list(cursor.fetchone())
        conn.close()
        return account.objects.get(user=User.objects.get(username=user[4]))
    except:
        return None

def get_conn():
    conn = sqlite3.connect('./db.sqlite3')
    return conn

def get_token():
    try:
        with open("./tele_bot/telebot.json") as f:
            return json.load(f)['token']
    except FileNotFoundError:
        raise Exception("File with token does not found.")
    except KeyError:
        raise Exception("Token is not defined.")

BOT_TOKEN = get_token()
bot = telebot.TeleBot(BOT_TOKEN)

def create_inline_keyboard(buttons):
    """Создает inline-клавиатуру с указанными кнопками."""
    keyboard = types.InlineKeyboardMarkup()
    for button_text, button_data in buttons:
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=button_data))
    return keyboard

def create_reply_keyboard(buttons):
    """Создает reply-клавиатуру с указанными кнопками."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button_text, button_data in buttons:
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=button_data))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start. Проверяет авторизацию пользователя."""
    user_id = message.from_user.id
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_user WHERE telegramm_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Пользователь уже авторизован
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=create_inline_keyboard([
            ('Мой счёт', 'cnt'),
            ('Законы ЛЕСограда', 'rools'),
            ('Расписание', 'plan'),
            ('Задачи дня', 'quests'),
            ('Товары', 'goods'),
            ('Ссылка', 'link'),
        ]))
    else:
        # Пользователь не авторизован, предлагаем авторизоваться
        bot.send_message(message.chat.id, "Пожалуйста, авторизуйтесь.", reply_markup=create_inline_keyboard([
            ('Авторизация', 'login'),
            ('Помощь', 'help')
        ]))

@bot.message_handler(commands=['logout'])
def logout(message):
    """Обработчик команды /logout. Проверяет авторизацию пользователя."""
    user_id = message.from_user.id
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_user WHERE telegramm_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Пользователь уже авторизован
        conn = get_conn()
        conn.cursor().execute("UPDATE auth_user SET telegramm_id = ? WHERE username = ?", ("", list(user)[4]))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Вы вышли из аккаунта.", reply_markup=create_inline_keyboard([
            ('Авторизация', 'login'),
            ('Помощь', 'help')
        ]))
    else:
        # Пользователь не авторизован
        bot.send_message(message.chat.id, "Вы уже успешно вышли!", reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))

@bot.message_handler(commands=['login'])
def login(message):
    """Обработчик авторизации."""
    user_id = message.from_user.id
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_user WHERE telegramm_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        bot.send_message(message.chat.id, f"Вы уже авторизованы как {get_acc(message.from_user.id)}.", reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
        return
    bot.send_message(message.chat.id, "Введите ваш логин:", reply_markup=create_reply_keyboard([
        ('Войти', 'login'),
        ('Выйти', 'logout'),
        ('Ссылка', 'link'),
        ('Помощь', 'help'),
    ]))
    bot.register_next_step_handler(message, process_username)

def process_username(message):
    """Получает логин пользователя."""
    username = message.text
    bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(message, process_password, username)

def process_password(message, username):
    """Получает пароль пользователя."""
    password = message.text
    user_id = message.from_user.id
    try:
        user_bank = User.objects.get(username=username)
    except:
        user_bank = None
    if user_bank:
        if user_bank.check_password(password):
            # Авторизация успешна
            conn = get_conn()
            conn.cursor().execute("UPDATE auth_user SET telegramm_id = ? WHERE username = ?", (user_id, username))
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Авторизация прошла успешно!", reply_markup=create_inline_keyboard([
                ('Мой счёт', 'cnt'),
                ('Законы ЛЕСограда', 'rools'),
                ('Расписание', 'plan'),
                ('Задачи дня', 'quests'),
                ('Товары', 'goods'),
                ('Ссылка', 'link'),
            ]))
        else:
            # Неверный пароль
            bot.send_message(message.chat.id, "Неверный пароль.")
    else:
        # Неверный логин
        bot.send_message(message.chat.id, "Неверный логин.")

@bot.message_handler(commands=['cnt'])
def cnt(message, user_id=None):
    if user_id is None: user_id = message.from_user.id
    s = ""
    acc = get_acc(user_id)
    if acc is None:
        bot.send_message(message.chat.id, "Вам нужно войти в аккаунт.", reply_markup=create_inline_keyboard([
            ('Авторизация', 'login'),
            ('Помощь', 'help')
        ]))
        return
    for i in transaction.objects.filter(Q(receiver=acc) | Q(creator=acc)):
        if '-' in i.sign and i.receiver == acc: x = '-'
        elif '+' in i.sign and i.creator == acc: x = '-'
        else: x = '+'
        s += f'{i.get_type_of()}: {x}{i.get_sum()} (Создал {i.history}, {i.date}); {i.comment}\n'
    bot.send_message(message.chat.id, f"Ваш счёт: {acc.balance}t", reply_markup=create_reply_keyboard([
        ('Войти', 'login'),
        ('Выйти', 'logout'),
        ('Ссылка', 'link'),
        ('Помощь', 'help'),
    ]))
    if s == '':
        bot.send_message(message.chat.id, "У вас нет переводов.")
    else:
        MESS_MAX_LENGTH = 4096
        for x in range(0, len(s), MESS_MAX_LENGTH):
            mess = s[x: x + MESS_MAX_LENGTH]
            bot.send_message(message.chat.id, mess)
        bot.send_message(message.chat.id, "Что ещё вас интересует?", reply_markup=create_inline_keyboard([
            ('Мой счёт', 'cnt'),
            ('Законы ЛЕСограда', 'rools'),
            ('Расписание', 'plan'),
            ('Задачи дня', 'quests'),
            ('Товары', 'goods'),
            ('Ссылка', 'link'),
        ]))

@bot.message_handler(commands=['rool'])
def rool(message):
    s = ""
    for i in rools.objects.all():
        if i.is_costable():
            s += f'{i}; {i.punishment}, {i.get_cost()}\n'
        else:
            s += f'{i}; {i.punishment}, {i.get_cost()}\n'
    MESS_MAX_LENGTH = 4096
    for x in range(0, len(s), MESS_MAX_LENGTH):
        mess = s[x: x + MESS_MAX_LENGTH]
        bot.send_message(message.chat.id, mess, reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
    bot.send_message(message.chat.id, "Что ещё вас интересует?", reply_markup=create_inline_keyboard([
        ('Мой счёт', 'cnt'),
        ('Законы ЛЕСограда', 'rools'),
        ('Расписание', 'plan'),
        ('Задачи дня', 'quests'),
        ('Товары', 'goods'),
        ('Ссылка', 'link'),
    ]))

@bot.message_handler(commands=['plan'])
def plans(message):
    s = ""
    for i in plan.objects.all():
        s += f'{i}\n'
    MESS_MAX_LENGTH = 4096
    for x in range(0, len(s), MESS_MAX_LENGTH):
        mess = s[x: x + MESS_MAX_LENGTH]
        bot.send_message(message.chat.id, mess, reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
    bot.send_message(message.chat.id, "Что ещё вас интересует?", reply_markup=create_inline_keyboard([
        ('Мой счёт', 'cnt'),
        ('Законы ЛЕСограда', 'rools'),
        ('Расписание', 'plan'),
        ('Задачи дня', 'quests'),
        ('Товары', 'goods'),
        ('Ссылка', 'link'),
    ]))

@bot.message_handler(commands=['quests'])
def quests(message):
    b = False
    for i in daily_answer.objects.all():
        b = True
        s = f'{i}\n\n' + f'{i.text}\n\n' + f'{"Вопрос смены" if i.status else "Вопрос дня"}'
        bot.send_message(message.chat.id, s, reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
    if not b:
        bot.send_message(message.chat.id, "Ежедневных задач ещё нет.", reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
    bot.send_message(message.chat.id, "Что ещё вас интересует?", reply_markup=create_inline_keyboard([
        ('Мой счёт', 'cnt'),
        ('Законы ЛЕСограда', 'rools'),
        ('Расписание', 'plan'),
        ('Задачи дня', 'quests'),
        ('Товары', 'goods'),
        ('Ссылка', 'link'),
    ]))

@bot.message_handler(commands=['goods'])
def goods(message):
    b = False
    for i in good.objects.all():
        b = True
        s = f'{i.name} ({i.comment}) - {i.get_num()}'
        bot.send_message(message.chat.id, s, reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
    if not b:
        bot.send_message(message.chat.id, "Товаров пока нет.", reply_markup=create_reply_keyboard([
            ('Войти', 'login'),
            ('Выйти', 'logout'),
            ('Ссылка', 'link'),
            ('Помощь', 'help'),
        ]))
    bot.send_message(message.chat.id, "Что ещё вас интересует?", reply_markup=create_inline_keyboard([
        ('Мой счёт', 'cnt'),
        ('Законы ЛЕСограда', 'rools'),
        ('Расписание', 'plan'),
        ('Задачи дня', 'quests'),
        ('Товары', 'goods'),
        ('Ссылка', 'link'),
    ]))

@bot.message_handler(commands=['link'])
def link(message):
    s = "Сслыка для доступа на сайт:\n\n" \
    f"{get_link4bot()}\n\n" \
    "Приятного пользования!"
    bot.send_message(message.chat.id, s, reply_markup=create_reply_keyboard([
        ('Войти', 'login'),
        ('Выйти', 'logout'),
        ('Ссылка', 'link'),
        ('Помощь', 'help'),
    ]))
    bot.send_message(message.chat.id, "Что ещё вас интересует?", reply_markup=create_inline_keyboard([
        ('Мой счёт', 'cnt'),
        ('Законы ЛЕСограда', 'rools'),
        ('Расписание', 'plan'),
        ('Задачи дня', 'quests'),
        ('Товары', 'goods'),
        ('Ссылка', 'link'),
    ]))

@bot.message_handler(commands=['help'])
def help(message):
    s = "Команды:\n\n" \
        "/start - Запуск бота;\n" \
        "/login - Вход в аккаунт от банка;\n" \
        "/logout - Выход из аккаунта от банка;\n" \
        "/cnt - Посмотреть свой счёт;\n" \
        "/rools - Посмотреть законы ЛЕСограда;\n" \
        "/plan - Посмотреть расписание;\n" \
        "/quests - Ежедневные задачи;\n" \
        "/goods - Товары;\n" \
        "/link - Ссылка на сайт в интернете."
    bot.send_message(message.chat.id, s, reply_markup=create_inline_keyboard([
        ('Мой счёт', 'cnt'),
        ('Законы ЛЕСограда', 'rools'),
        ('Расписание', 'plan'),
        ('Задачи дня', 'quests'),
        ('Товары', 'goods'),
        ('Ссылка', 'link'),
    ]))

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Войти':
        login(message)
        return
    if message.text == 'Выйти':
        logout(message)
        return
    if message.text == 'Ссылка':
        link(message)
        return
    if message.text == 'Помощь':
        help(message)
        return

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Обработчик нажатия на кнопки inline-клавиатуры."""
    match call.data:
        case 'login':
            login(call.message)
        case 'logout':
            logout(call.message)
        case 'cnt':
            cnt(call.message, call.from_user.id)
        case 'rools':
            rool(call.message)
        case 'plan':
            plans(call.message)
        case 'quests':
            quests(call.message)
        case 'goods':
            goods(call.message)
        case 'help':
            help(call.message)
        case 'link':
            link(call.message)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
