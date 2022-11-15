import sqlalchemy
import telebot
from telebot import types

from tgbot import config
from create_table import db, connection

bot = telebot.TeleBot(config.TOKEN)

user_dict = {}


class User:
    def __init__(self):
        self.task_dict = []


class Task:
    def __init__(self, number):
        self.number = number
        self.name = None
        self.description = None
        self.deadline = None


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    chat_id = message.chat.id
    user_dict[chat_id] = User()


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtnaddtask = types.KeyboardButton('Добавить задачу')
    itembtnshowtask = types.KeyboardButton('Просмотреть задачу')
    markup.add(itembtnaddtask, itembtnshowtask)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    # ReplyKeyboardRemove: hides a previously sent ReplyKeyboardMarkup
    # Takes an optional selective argument (True/False, default False)
    # markup = types.ReplyKeyboardRemove(selective=False)
    # bot.send_message(message.chat.id, message, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def action(message):
    if message.text == 'Добавить задачу':
        msg = bot.reply_to(message, 'Введите название задачи:')
        bot.register_next_step_handler(msg, process_task_name)
    elif message.text == 'Просмотреть задачу':
        chat_id = message.chat.id
        user = user_dict[chat_id]
        task_dict = user.task_dict
        tasks = ''
        for task in task_dict:
            tasks += str(task.number) + '. ' + task.name + '\n' + task.description + '\nСрок: ' + task.deadline + '\n'
        bot.send_message(message.chat.id, 'Список задач:\n\n' + tasks + '\nВыберите задачу:')


@bot.message_handler(content_types=['text'])
def process_task_name(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    number = len(user.task_dict)
    user.task_dict.append(Task(number + 1))
    task = user.task_dict[number]
    name = message.text
    task.number = number
    task.name = name
    msg = bot.reply_to(message, 'Добавим описание задачи:')
    bot.register_next_step_handler(msg, process_task_description)


@bot.message_handler(content_types=['text'])
def process_task_description(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    number = len(user.task_dict) - 1
    task = user.task_dict[number]
    description = message.text
    task.description = description
    msg = bot.reply_to(message, 'И на последок дедлайн:')
    bot.register_next_step_handler(msg, process_task_deadline)


@bot.message_handler(content_types=['text'])
def process_task_deadline(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    number = len(user.task_dict) - 1
    task = user.task_dict[number]
    deadline = message.text
    task.deadline = deadline
    bot.send_message(message.chat.id, 'Задание успешно добавлено!')


def run():
    bot.infinity_polling()


run()
