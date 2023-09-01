# Банк ЛИС

## Я вдохновлялся и использовал как образец данные репозитории: https://github.com/RegSirius06/lisbank и https://github.com/RegSirius06/messenger_for_LFMSH

## Комментарий по поводу эксплуатации проекта

Я рекомендую вам использовать именно данную конфигурацию сайта, с данной базой данных. В ней только один пользователь, он же и супер-юзер.

Логин: admin
Пароль: admin

Сменить пароль можно на admin-панели (её адрес, например, localhost:8000/admin/) в разделе "Пользователи".
Нельзя менять логин этого пользователя, группы, в которых он состоит, фамилию, имя, отчество, пользователя, отряд в аккаунте, связанном с этим пользователем.

Тем не менее, вы можете создать свою базу данных с нуля. В таком случае:

1) Создайте суперпользователя с логином admin.
2) Запустите сайт
3) Войдите в админ-панель сайта
4) Добавьте аккаунт (в разделе "Accounts") с привязкой к созданному пользователю, с обязательным заполнением именно таким образом следующих панелей:

Пользователь: admin
Имя: BANK
Отчество: BANK
Фамилия: Admin
Отряд: 0

Остальные поля заполняйте на ваше усмотрение.

После успешной регистрации пользователя можно перейти непосредственно в банк (по адресу, например, "localhost:8000").

## Интерфейс банка и админ-панели

Интерфейс банка и админ-панели интуитивно понятен. Все транзакции и пользователи нужно изменять/добавлять именно на сайте, а не в admin-панели, чтобы не возникло проблем.

Для разрешения переводов средств для учатсников смены нужно в группе "listener" добавить разрешение "Может совершать переводы". Если вы регистрировали пользователей автоматически на сайте, то у вас не должно возникнуть проблем с этим.

Чтобы добавить человека в мерию (в ЛИСе такое есть), нужно зайти в admin-панель, найти его аккаунт в списке пользователей ("Пользователи", не "Accounts") и добавить к пользователю группу "meria". Отозвать права можно аналогичным образом.

Только поле "Roolss" admin-панели заполняется в admin-панели, всё остальное создаётся автоматически на сайте.

## Как использовать

Нужно установить Python 3.11 и младше, если вы этого не сделали.

Установить Django:

#### pip install Django

Я использовал Django 4.2.2, если стоит версия новее, то ничего страшного.

Проверить версию можно, запустив файл /lisbank/django_ver.py

Затем нужно изменить одну строчку в /lisbank/settings.py. Она почти в самом конце файла:

### STATIC_URL = 'static/'
### STATIC_ROOT = 'C:/LisBank/lisbank/bank/static/'

В STATIC_ROOT необходимо вбить путь до папки static на вашем устройсте, например:

### STATIC_ROOT = 'D:/lisbank/bank/static/'

Учтите, что путь должен оканчиваться на "/bank/static/".

Если это изменение не внести, то, скорее всего, дизайн сайта пострадает очень сильно

В консоли перейти в папку, где есть файл "manage.py" и запустить его командой:

#### python .\manage.py runserver 0.0.0.0:8000 --insecure

Сайт доступен в локальной сети по адресу "192.168.50.40:8000", если адрес вашего ПК в локальной сети "192.168.50.40".

## Регистрация пользователей

Пользователей можно зарегистрировать в разделе "Работа с пользователями". После регистрации его логин и пароль будут записаны в в файл "All_users.txt". Обратите внимание, что при удалении пользователя запись о нём в файле остаётся.

При сбросе всех паролей будут обновлены пароли у всех пользователей, логин которых не содержит текста "admin". После сброса паролей обновлённый список будет находиться в файле "All_users.txt".

## Хорошего пользования!
