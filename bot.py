import telebot
import config
from telebot import types
from handlers import main_menu, main_menu_check, send_menu_check, send_message_menu, send_message_menu_check, choose_users, \
    choose_users_check, confirm, confirm_check, choose_users_id, choose_users_id_check, choose_users_period, choose_users_period_check, \
    analytic_menu_check

bot = telebot.TeleBot(config.TOKEN)
status = -1  # -1 - bot off; 0 - main menu;

@bot.message_handler(commands=['start'])
def welcome(message):
    global status
    status = 0
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, \nДля взаимодействия со мной можешь воспользоваться меню или использовать текстовые команды. \n".format(
                         message.from_user, bot.get_me()), parse_mode='html')
    status = main_menu(message)

@bot.message_handler(commands=['stop'])
def stop(message):
    global status
    # bot.send_message(message.chat.id, 'Бот остановлен', reply_markup=telebot.types.ReplyKeyboardRemove())
    status = -1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton('/start')
    markup.add(item_start)
    bot.send_message(message.chat.id, "Бот остановлен", reply_markup=markup)

@bot.message_handler(
    content_types=['audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice',
                   'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment', 'connected_website', 'poll',
                   'passport_data', 'web_app_data'])
def repeat(message):
    bot.send_message(message.chat.id, 'Пожалуйста, пришлите верную текстовую команду', parse_mode='html')

@bot.message_handler(content_types = "text")
def repeat(message):
    global status
    print('status = ', status)
    if status == 1:
        status = main_menu_check(message)
        return 0
    if status == 2:
        status = send_menu_check(message)
        return 0
    if status == 3:
        status = send_message_menu(message, message.text)
        return 0
    if status == 4:
        status = send_message_menu_check(message)
        return 0
    if status == 5:
        status = choose_users(message)
        return 0
    if status == 6:
        status = choose_users_check(message)
        return 0
    if status == 7:
        status = choose_users_id_check(message)
        return 0
    if status == 8:
        status = choose_users_period_check(message)
        return 0
    if status == 9:
        status = confirm_check(message)
        return 0
    if status == 10:
        status = analytic_menu_check(message)
        return 0

#RUN
print('successfully started')
bot.polling(non_stop=True)
print('successfully stopped')