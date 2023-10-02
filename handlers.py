import telebot
import config
import re
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
text_to_send = ''
group_number = -1
id_to_send = []
period = 0
flag = ''

def main_menu(message):
    global status
    status = 1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_send = types.KeyboardButton('Отправить сообщение')
    item_analytics = types.KeyboardButton('Посмотреть аналитику')
    item_exit = types.KeyboardButton('/stop')
    markup.add(item_send, item_analytics, item_exit)

    bot.send_message(message.chat.id, "Открыто главное меню", reply_markup=markup)
    return status

def main_menu_check(message):
    global status
    if message.text == "Посмотреть аналитику":
        status = analytic_menu(message)
    elif message.text == "Отправить сообщение":
        status = send_menu(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите верную команду')
    return status

def analytic_menu(message):
    global status
    status = 10
    keyboard_anal = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_5_1 = types.KeyboardButton('Топ 10 богатых пользователей')
    key_5_2 = types.KeyboardButton('Что-то ещё')
    key_5_3 = types.KeyboardButton('Назад')
    keyboard_anal.add(key_5_1, key_5_2, key_5_3)

    bot.send_message(message.chat.id,
                     'Выберете аналитику для отчёта',
                     reply_markup=keyboard_anal)
    return status

def analytic_menu_check(message):
    global status
    if message.text == 'Топ 10 богатых пользователей':
        bot.send_message(message.chat.id, 'Вывод топ 10 богатых пользователей')
        # место для запроса к БД
        status = main_menu(message)
    elif message.text == 'Что-то ещё':
        bot.send_message(message.chat.id, 'Вывод чего-то ещё')
        # место для запроса к БД
        status = main_menu(message)
    elif message.text == 'Назад':
        status = main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, пришлите верную команду')

    return status

def send_menu(message):
    global status
    status = 2
    keyboard_send = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_1_1 = types.KeyboardButton('Создать')
    key_1_2 = types.KeyboardButton('Выбрать (заглушка)')
    key_1_3 = types.KeyboardButton('Назад')
    keyboard_send.add(key_1_1, key_1_2, key_1_3)

    bot.send_message(message.chat.id, 'Выберите: вы хотите создать новое сообщение или выбрать для отправки существующее', reply_markup=keyboard_send)
    return status

def send_menu_check(message):
    global status
    if message.text == "Создать":
        bot.send_message(message.chat.id, 'Введите сообщение для отправки', reply_markup = types.ReplyKeyboardRemove())
        status = 3
    elif message.text == "Выбрать (заглушка)":
        bot.send_message(message.chat.id, 'Раздел находится в разработке')
    elif message.text == "Назад":
        status = main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Введите верную команду, пожалуйста')
    return status

def send_message_menu(message, text):
    global status
    global text_to_send
    status = 4
    text_to_send = text
    keyboard_prepare = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_2_1 = types.KeyboardButton('Отправить')
    key_2_2 = types.KeyboardButton('Отредактировать')
    key_2_3 = types.KeyboardButton('Проверить')
    keyboard_prepare.add(key_2_1, key_2_2, key_2_3)
    bot.send_message(message.chat.id, 'Ваш текущий текст: ' + text, reply_markup = keyboard_prepare)

    return status

def send_message_menu_check(message):
    global status
    if message.text == 'Проверить':
        bot.send_message(message.chat.id, 'Ваш текущий текст: ' + text_to_send)
    elif message.text == 'Отредактировать':
        bot.send_message(message.chat.id, 'Введите сообщение для отправки', reply_markup = types.ReplyKeyboardRemove())
        status = 3
    elif message.text == 'Отправить':
        status = choose_users(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, пришлите верную команду')
    return status

def choose_users(message):
    global status
    status = 6
    keyboard_users = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_3_1 = types.KeyboardButton('Выбрать по ID')
    key_3_2 = types.KeyboardButton('Выбрать по периоду активности')
    keyboard_users.add(key_3_1, key_3_2)
    bot.send_message(message.chat.id, 'Выберете способ фильтрации пользователей', reply_markup = keyboard_users)
    return status

def choose_users_check(message):
    global status
    global group_number
    global id_to_send
    global flag
    if message.text == 'Выбрать по ID':
        flag = 'ID'
        id_to_send = []
        status = choose_users_id(message)
    elif message.text == 'Выбрать по периоду активности':
        flag = 'period'
        status = choose_users_period(message)
    else:
        bot.send_message(message.chat.id, 'Выберете одно из предложенных действий')
    return status

def choose_users_id(message):
    global status
    status = 7
    bot.send_message(message.chat.id, 'Присылайте ID пользователей. Каждое ID в отдельном сообщении. Чтобы закончить ввод и подтвердить выбор пришлите 0', reply_markup = types.ReplyKeyboardRemove())
    return status

def choose_users_id_check(message):
    global status
    global id_to_send
    id = message.text
    if id != '0':
        id_to_send.append(message.text)
    else:
        status = confirm(message)
    return status

def check_date(str):
    #check for format DD.MM.YYYY
    pattern_str = r'^\d{2}-\d{2}-\d{4}$'
    if re.match(pattern_str, str):
        return True
    else:
        return False

def choose_users_period(message):
    global status
    status = 8
    bot.send_message(message.chat.id, 'Введите дату начала периода, за который хотите отправить сообщение. Формат: DD-MM-YYYY')
    return status

def choose_users_period_check(message):
    global status
    global period
    if check_date(message.text):
        period = message.text
        status = confirm(message)
    else:
        bot.send_message(message.chat.id, 'Пришлите, пожалуйста, дату в верном формате')
    return status

def confirm(message):
    global status
    global id_to_send
    global flag
    status = 9
    keyboard_confirm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_4_1 = types.KeyboardButton('Да')
    key_4_2 = types.KeyboardButton('Нет')
    keyboard_confirm.add(key_4_1, key_4_2)
    if flag == 'ID':
        bot.send_message(message.chat.id, 'Отправить сообщение с текстом:\n' + text_to_send + '\nГруппе пользователей c ID: ' + str(set(id_to_send)) + '\n',  reply_markup = keyboard_confirm)
    if flag == 'period':
        bot.send_message(message.chat.id,
                         'Отправить сообщение с текстом:\n' + text_to_send + '\nГруппе пользователей, которые проявляли активность за период, начиня с: ' + str(period) + '\n', reply_markup=keyboard_confirm)
    return status

def confirm_check(message):
    global status
    if message.text == 'Да':
        if flag == 'ID':
            bot.send_message(message.chat.id, 'Тут происходит отправка сообщения по id')
            # место для вызова функции из реального бота
        if flag == 'period':
            bot.send_message(message.chat.id, 'Тут происходит отправка сообщения по period')
            # место для вызова функции из реального бота
        status = main_menu(message)
        #send_mes
    elif message.text == 'Нет':
        status = send_menu(message)
    else:
        bot.send_message(message.chat.id, 'Введите корректную команду')
    return status