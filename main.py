import telebot
from telebot import types
from constants import TOKEN, ENGINE
from database import User, Task
from sqlalchemy.orm import sessionmaker

bot = telebot.TeleBot(TOKEN, parse_mode=None)

session = sessionmaker(bind=ENGINE)
s = session()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Welcome, {0.first_name}!'.format(message.from_user))
    if not s.query(s.query(User).filter(User.telegram_id == message.from_user.id).exists()).scalar():
        s.add(User(telegram_id=message.from_user.id, username=message.from_user.username))
        s.commit()
    show_main_menu(message)


def get_current_user_id(message):
    current_user = s.query(User).filter(User.telegram_id == message.from_user.id).first()
    return current_user.telegram_id


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Add a task')
    item2 = types.KeyboardButton('Show tasks')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Add a task')
def add_task(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    message = bot.send_message(message.chat.id, 'Enter the name:', reply_markup=markup)
    bot.register_next_step_handler(message, set_name)


def set_name(message):
    task = Task(user_id=get_current_user_id(message), name=message.text, is_completed=False)
    s.add(task)
    s.flush()
    current_task_id = task.id
    s.commit()
    message = bot.send_message(message.chat.id, 'Enter the description:')
    bot.register_next_step_handler(message, set_description, current_task_id)


def set_description(message, current_task_id):
    s.query(Task).filter(Task.id == current_task_id).update({'description': message.text})
    s.commit()
    bot.send_message(message.chat.id, 'Enter the deadline in YY-MM-DD HH:MM format or type any letter to create a '
                                      'task without a deadline')
    bot.register_next_step_handler(message, set_deadline, current_task_id)


def set_deadline(message, current_task_id):
    try:
        s.query(Task).filter(Task.id == current_task_id).update({'deadline': message.text})
        s.commit()
    except:
        bot.reply_to(message, 'You entered the date/time incorrectly or you wanted it to be empty, so the task was '
                              'created without it.')
    finally:
        show_main_menu(message)


@bot.message_handler(func=lambda message: message.text == 'Show tasks')
def show_tasks(message):
    bot.send_message(message.chat.id, 'Your tasks:')


bot.polling()
