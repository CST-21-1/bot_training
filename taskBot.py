from telebot import *
from telebot.ext import *
from requests import *

bot = telebot.TeleBot('5741260025:AAEUYgaP6f1ULfHe9gbsViVZ_XEJn0DjhGA')



@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.reply_to(message, "Welcome, this is tasklist bot!")
	show_main_options(message)

def show_main_options(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	addTaskButton = types.KeyboardButton('Add new task')
	showTasksButton = types.KeyboardButton('Show tasks')
	markup.row(addTaskButton, showTasksButton)

	mess = bot.send_message(message.chat.id, "Press one of the buttons" ,reply_markup=markup)
	bot.register_next_step_handler(mess, process_main_options)


def process_main_options(message):
	messageText = message.text
	if messageText == 'Add new task':
		bot.send_message(message.chat.id, "No functionality for this button yet")
		#TODO: Make logic for receiving data from the user
		show_main_options(message)
	elif messageText == 'Show tasks':
		# TODO: Make logic for showing tasks to the user
		bot.send_message(message.chat.id, "No functionality for this button too")
		show_main_options(message)
	else:
		mess = bot.send_message(message.chat.id, "Unknown functions, please, choose only stated options!")
		show_main_options(message)

bot.infinity_polling()