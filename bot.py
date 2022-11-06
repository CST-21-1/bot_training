import telebot
from telebot import types

bot = telebot.TeleBot("5601781209:AAG3s3u92TYLSmkOAGz6f9Pp4H1pelyr9fQ")

data = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi. This is task manager.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_create_task = types.KeyboardButton('Create task')
    item_view_tasks = types.KeyboardButton('View tasks')

    markup.add(item_create_task, item_view_tasks)
    bot.send_message(message.chat.id, "ok", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def do_option(message):
    user_id = message.from_user.id
    if message.text == 'Create task':
        data.append(user_id)
        bot.send_message(message.chat.id, 'Write the name of the task')
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'View tasks':
        bot.send_message(message.chat.id, str(data))


def get_name(message):
    data.append(message.text)
    bot.send_message(message.chat.id, 'Write the description of the task')
    bot.register_next_step_handler(message, get_description)


def get_description(message):
    data.append(message.text)
    bot.send_message(message.chat.id, 'Write the deadline of the task')
    bot.register_next_step_handler(message, get_deadline)


def get_deadline(message):
    data.append(message.text)
    bot.register_next_step_handler(message, send_welcome)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'create_task':
        pass
    elif call.data == 'view_tasks':
        pass


bot.polling(none_stop=True, interval=0)
