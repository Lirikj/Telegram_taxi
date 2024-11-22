from telebot import types 
from baza import user_exists, add_user_to_db
from config import bot


@bot.message_handler(commands=['start', 'st', 'mn', 'menu'])
def start_message(message):
    user = message.from_user
    user_id = message.from_user.id
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ''
    username = message.from_user.username

    if user_exists(user_id): 
        markup = types.InlineKeyboardMarkup(row_width=1) 
        web_app = types.WebAppInfo("https://lirikj.github.io/webapp.github.io/") 
        web_app_button = types.KeyboardButton('🚖Заказать такси🚖', web_app=web_app )
        markup.add(web_app_button)
        bot.send_message(message.chat.id, f'Привет, {first_name}'
                        '\n '
                        '\nдля вызова такси перейди в приложение', reply_markup=markup)
    else: 
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        get_phone = types.KeyboardButton('📞Ваш номер', request_contact=True) 
        markup.add(get_phone)
        number = bot.send_message(message.chat.id, 
                                  '🚕Привет, я бот для заказа такси.'
                                  '\n'
                                  '\nЧтоб заказать такси мне нужен твой номер телефона, надеюсь ты не против?', 
                                  reply_markup=markup) 
        bot.register_next_step_handler(number, registration_user, user_id, username, first_name, last_name) 


def registration_user(message, user_id, username, first_name, last_name):
    if message.contact is not None:
        phone_number = message.contact.phone_number
        add_user_to_db(user_id, username, first_name, last_name, phone_number)
        bot.send_message(message.chat.id, 'Спасибо! Ваш номер добавлен.')
    else:
        number = bot.send_message(message.chat.id, 'Ошибка: номер телефона не был передан.')
        bot.register_next_step_handler(number, registration_user, user_id, username, first_name, last_name) 


@bot.message_handler(commands=['info', 'developers']) 
def info(message):
    bot.send_message(message.chat.id, '👨🏼‍💻developer - @Lirikj'
                                    '\n🧑🏻‍💻developer - @NFCshka')




bot.polling()