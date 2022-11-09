import telebot
from telebot import types

TOKEN = '5600387192:AAHpc1Nyt5NJQ6WzhadeB1uOZBBkEDEPjCU'

bot = telebot.TeleBot(TOKEN, parse_mode=None)


names = []
descriptions = []
deadlines = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Welcome, {0.first_name}!'.format(message.from_user))
    show_main_menu(message)


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("Add a task")
    item2 = types.KeyboardButton("Show tasks")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Would you like to ...', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def add_task(message):
    if message.text == 'Add a task':
        markup = types.ReplyKeyboardRemove(selective=False)
        message = bot.send_message(message.chat.id, 'Enter the name:', reply_markup=markup)
        bot.register_next_step_handler(message, set_name)


def set_name(message):
    names.append(message.text)
    print(names)
    message = bot.send_message(message.chat.id, 'Enter the description:')
    bot.register_next_step_handler(message, set_description)


def set_description(message):
    descriptions.append(message.text)
    print(descriptions)
    bot.send_message(message.chat.id, 'Enter the deadline:')
    bot.register_next_step_handler(message, set_deadline)


def set_deadline(message):
    deadlines.append(message.text)
    print(deadlines)
    show_main_menu(message)


@bot.message_handler(content_types=['text'])
def show_tasks(message):
    if message.text == 'Show tasks':
        bot.send_message(message.chat.id, 'Your tasks: ')


bot.polling()
