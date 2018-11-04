import secure, time, json, VKToolKit, pickle, os, threading, re
from pyrogram import *

bot = Client(secure.token, secure.api_id, secure.api_hash)

file = open('alist', 'r')
alist = json.load(file)
file.close()
file = open('users', 'r')
users = json.load(file)
file.close()

print(alist)


def reset(id):
    try:
        os.remove(str(id))
    except Exception:
        pass
    try:
        alist.remove(id)
    except Exception:
        pass
    bot.send_message(id, 'Сброшено.')


class User:
    def __init__(self, tg_id):
        self.tg_id = tg_id
        self.vk_login = None
        self.vk_pass = None
        self.vk_token = None
        self.vk_id = None
        self.current_status = None
        self.current_song = None

    def refresh(self):
        file = open(str(self.tg_id), 'wb')
        pickle.dump(self, file)
        file.close()


def status(tg_id):
    user = user_get(tg_id)
    ans = 'Текущее состояние Вашего аккаунта:\n\n' \
          '**Telegram ID**\n     ```' + str(user.tg_id) + '```\n' \
          '**VK ID** \n     ```' + str(user.vk_id) + '```\n' \
          '**VK Login** \n     ```' + str(user.vk_login) + '```\n' +\
          '**VK Password** \n     ```' + str(user.vk_pass) + '```\n' \
          '**Status** \n     ```' + str(user.current_status) + '```\n' \
          '**Song** \n     ```' + str(user.current_song) + '``` \n'
    return ans


def user_get(tg_id):
    try:
        file = open(str(tg_id), 'rb')
        user = pickle.load(file)
        file.close()
    except FileNotFoundError:
        file = open(str(tg_id), 'wb')
        user = User(tg_id)
        pickle.dump(user, file)
        file.close()
    return user

"""



@bot.on_message(Filters.command("save") & Filters.private)
def on_start(client, msg):
    file = open('alist', 'w')
    json.dump(alist, file)
    file.close()
    bot.send_message(msg.from_user.id, 'ОК')


@bot.on_message(Filters.command("help") & Filters.private)
def on_start(client, msg):
    ans = 'Привет. Я - бот, который установит тебе автостатус для ВК.' \
          'Теперь на твоей странице всегда будет какой-то трек. Какой - решать тебе!' \
          '\n\n**Как начать работу?**\n' \
          '    `Отправь мне данные для авторизции в формате логин:пароль. Далее следуй инструкциям.`' \
          '\n\n**Почему не токен?**\n    `Потому что ВКонтакте закрыл доступ для обычных токенов. ' \
          'Я же притворяюсь офф приложением. С удовольствием бы добавил авторизацию по токену ради доверия, ' \
          'но это невозможно из-за ВК`' \
          '\n\n**Что-то пошло не так, как мне все сбросить?**\n    `Команда /reset удаляет все, что связано с твоим ' \
          'аккаунтом с моих серверов`'
    bot.send_message(msg.chat.id, ans)


@bot.on_message(Filters.command('mytoken') & Filters.private)
def somedef(client, msg):
    a = user_get(msg.from_user.id)
    bot.send_message(msg.chat.id, 'Ваш авторизованный токен -> ' + str(a.vk_token))


@bot.on_message(Filters.command('reset') & Filters.private)
def somedef(client, msg):
    try:
        os.remove(str(msg.from_user.id))
    except Exception:
        pass
    try:
        alist.remove(msg.from_user.id)
    except Exception:
        pass
    bot.send_message(msg.chat.id, 'Сброшено.')


@bot.on_message(Filters.command('status') & Filters.private)
def somedef(client, msg):
    bot.send_message(msg.chat.id, 'Число активных пользователей: ')

"""


@bot.on_message(Filters.command("start") & Filters.private)
def on_start(client, msg):
    a = user_get(msg.chat.id)
    if a.current_status == None:
        ans = 'Привет. Всю информацию о боте ты можешь получить по команде' \
              ' /help.\nСейчас же отправь мне свои данные для авторизации типа LOGIN:PASSWORD, где LOGIN - Ваша почта\\номер телефона привязанные к аккаунту вк, и PASSWORD - Пароль от аккаунта'
        a.refresh()
        bot.send_message(msg.chat.id, ans)
    if msg.chat.id not in users:
        users.append(msg.chat.id)
    bot.send_message(msg.chat.id, 'm?')



@bot.on_message(Filters.command("help") & Filters.private)
def on_start(client, msg):
    ans = 'Привет. Я - бот, который установит тебе автостатус для ВК.' \
          'Теперь на твоей странице всегда будет какой-то трек. Какой - решать тебе!' \
          '\n\n**Как начать работу?**\n' \
          '    `Отправь мне данные для авторизции в формате логин:пароль. Далее следуй инструкциям.`' \
          '\n\n**Почему не токен?**\n    `Потому что ВКонтакте закрыл доступ для обычных токенов. ' \
          'Я же притворяюсь офф приложением. С удовольствием бы добавил авторизацию по токену ради доверия, ' \
          'но это невозможно из-за ВК`' \
          '\n\n**Что-то пошло не так, как мне все сбросить?**\n    `Команда /reset удаляет все, что связано с твоим ' \
          'аккаунтом с моих серверов`'
    bot.send_message(msg.chat.id, ans)


@bot.on_message(Filters.command("status") & Filters.private)
def help(client, msg):
    bot.send_message(msg.chat.id, status(msg.from_user.id))


@bot.on_message(Filters.command("save") & Filters.user(228348426))
def on_start(client, msg):
    file = open('alist', 'w')
    json.dump(alist, file)
    file.close()
    file = open('users', 'w')
    json.dump(users, file)
    file.close()
    bot.send_message(msg.from_user.id, 'ОК')


@bot.on_message(Filters.command("stop") & Filters.private)
def on_start(client, msg):
    try:
        alist.remove(msg.from_user.id)
        bot.send_message(msg.chat.id, 'Трансляция остановлена')
    except Exception:
        pass


@bot.on_message(Filters.command('reset') & Filters.private)
def somedef(client, msg):
    reset(msg.chat.id)


@bot.on_message(Filters.command('mytoken') & Filters.private)
def somedef(client, msg):
    a = user_get(msg.from_user.id)
    bot.send_message(msg.chat.id, 'Ваш токен - ' + a.vk_token)


@bot.on_message(Filters.command('an') & Filters.user(228348426))
def somedef(client, msg):
    text = msg.text[4:]
    print(users)
    print(text)
    for i in users:
        bot.send_message(i, text)

"""
   ВОТ ЭТОТ КОД НЕ РАБОТАЕТ 
@bot.on_message(Filters.text & Filters.private)
def somedef(client, msg):
    a = user_get(msg.from_user.id)
    if a.current_status == 'login_await':
        if True:
            bot.send_message(msg.chat.id, 'Логин получен, теперь мне нужен пароль!')
            a.current_status = 'UN|pass_await'
            a.vk_login = msg.text
            a.refresh()
    elif a.current_status == 'pass_await':
        if True:
            bot.send_message(msg.chat.id, 'Пароль получен!')
            a.vk_pass = msg.text
            a.refresh()

"""


@bot.on_message(Filters.text & Filters.private)
def somedef(client, msg):
    a = user_get(msg.from_user.id)
    if not a.current_status:
        bot.send_message(msg.chat.id, 'Данные получены, обрабатываю')
        try:
            auth = VKToolKit.auth(msg.text.split(':', maxsplit=1)[0], msg.text.split(':', maxsplit=1)[1])
        except IndexError:
            bot.send_message(msg.chat.id, 'Неверный формат данных, отправьте логин и пароль еще раз!')
            raise Exception
        if auth == '2fa_app' or auth == '2fa_sms':
            bot.send_message(msg.chat.id, 'Вам отправлен код 2FA. Отправьте его мне')
            a.current_status = '2FA_Await'
            a.vk_login = msg.text.split(':', maxsplit=1)[0]
            a.vk_pass = msg.text.split(':', maxsplit=1)[1]
            a.refresh()
        elif ['access_token'] in auth:
            a.vk_token = auth['access_token']
            a.current_status = 'OK'
            a.vk_pass = 'deleted'
            a.vk_login = 'deleted'
            a.vk_id = auth['user_id']
            bot.send_message(msg.chat.id, 'Успешно. Ваш токен:\n\n```' + auth['access_token'] + '```')
            bot.send_message(msg.chat.id, 'Теперь отправьте ссылку на песню, которую я помещу в ваш статус. Подробнее - /help')
            a.refresh()
    elif re.findall(r'\d{6}', msg.text) and a.current_status == '2FA_Await':
        code = msg.text
        bot.send_message(msg.chat.id, 'Код получен, идет обработка')
        auth = VKToolKit.auth_2fa(a.vk_login, a.vk_pass, code)
        if 'access_token' in auth:
            a.vk_token = auth['access_token']
            a.current_status = 'OK'
            a.vk_pass = 'deleted'
            a.vk_login = 'deleted'
            a.vk_id = auth['user_id']
            bot.send_message(msg.chat.id, 'Успешно. Ваш токен:\n\n```' + auth['access_token'] + '```')
            bot.send_message(msg.chat.id, 'Теперь отправьте ссылку на песню, которую я помещу в ваш статус. Подробнее - /help')
            a.refresh()
    elif msg.text.startswith('https://vk.com/audio') and bool(a.current_status == 'OK'):
        audio_id = msg.text[20:]
        a.current_song = audio_id
        a.refresh()
        if msg.from_user.id not in alist:
            alist.append(msg.from_user.id)
            print('Обновление алиста: ' + str(alist))
        bot.send_message(msg.chat.id, 'Успешно заменила песню.')


def cron():
    while True:
        time.sleep(55)
        for i in range(0, len(alist)):
            a = user_get(str(alist[i]))
            if a.current_status == 'OK' and a.current_song != None:
                print('')
                try:
                    VKToolKit.audio_broadcast(a.vk_token, a.current_song, str(a.vk_id))
                except Exception:
                    bot.send_message(a.tg_id, 'С вашими данными возникла проблема. Бот автоматически выполнил reset.'
                                              ' Авторизуйтесь заново')
                    reset(a.tg_id)


tokens_thread = threading.Thread(target=cron)
tokens_thread.start()
bot.run()






       
