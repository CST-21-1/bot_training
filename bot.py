import telebot
from telebot import types
from tgbot import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_table import Base, User, Task
from sqlalchemy.sql import exists

engine = create_engine('sqlite:///tasks-sqlalchemy.db', echo=True)
session = sessionmaker(bind=engine)
s = session()

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    # user = User(chat_id=message.chat.id)
    # s.add(user)
    # s.commit()
    chat_id = message.chat.id
    user = s.query(User.user_id).filter(User.chat_id == chat_id).all()
    if not user:
        user = User(chat_id=message.chat.id)
        s.add(user)
        s.commit()


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
        user_id = s.query(User.user_id).filter(User.chat_id == message.chat.id).one()
        # tasks = s.query(Task).filter(Task.user_id == user_id).group_by(Task.task_id)
        result = ''
        print('\n\n\nthis\n\n\n')
        for id, name, description, deadline in s.query(Task.task_id, Task.name, Task.description, Task.deadline).filter(Task.user_id == user_id).one(): #group_by(Task.task_id):
            result += str(id) + '. ' + name + '\n' + description + '\nСрок: ' + deadline + '\n'
        bot.send_message(message.chat.id, 'Список задач:\n\n' + result + '\nВыберите задачу:')


@bot.message_handler(content_types=['text'])
def process_task_name(message):
    name = message.text
    task = Task(name=name)
    msg = bot.reply_to(message, 'Добавим описание задачи:')
    bot.register_next_step_handler(msg, process_task_description, task)


@bot.message_handler(content_types=['text'])
def process_task_description(message, task):
    description = message.text
    task.description = description
    msg = bot.reply_to(message, 'И на последок дедлайн:')
    bot.register_next_step_handler(msg, process_task_deadline, task)


@bot.message_handler(content_types=['text'])
def process_task_deadline(message, task):
    deadline = message.text
    task.deadline = deadline
    user_id = s.query(User.user_id).filter(User.chat_id == message.chat.id)
    task.user_id = user_id
    bot.send_message(message.chat.id, 'Задание успешно добавлено!')
    s.add(task)
    s.commit()


def run():
    bot.infinity_polling()


run()
