import  os
from telebot import *
import taskBotDB
from dotenv import load_dotenv

load_dotenv()

#constants

greeting = "Welcome, this is tasklist bot!"

addTaskMessage = 'Add new task'

showTaskMessage = 'Show tasks'

noFuncMessage = "No functionality for this button yet"

unknownFuncMessage = "Unknown functions, please, choose only stated options!"

pressButtonMessage = "Press one of the buttons"


#start of the program

TOK = os.getenv("TOKEN")

bot = telebot.TeleBot(TOK)

botDB = taskBotDB.BotDB()

botDB.show_all_users()

@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.reply_to(message, greeting)
	show_main_options(message)


def show_main_options(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	addTaskButton = types.KeyboardButton(addTaskMessage)
	showTasksButton = types.KeyboardButton(showTaskMessage)
	markup.row(addTaskButton, showTasksButton)

	mess = bot.send_message(message.chat.id, pressButtonMessage ,reply_markup=markup)
	bot.register_next_step_handler(mess, process_main_options)


def process_main_options(message):
	messageText = message.text
	if messageText == addTaskMessage:
		bot.send_message(message.chat.id, noFuncMessage)
		#TODO: Make logic for receiving data from the user
		show_main_options(message)
	elif messageText == showTaskMessage:
		# TODO: Make logic for showing tasks to the user
		bot.send_message(message.chat.id, noFuncMessage)
		show_main_options(message)
	else:
		mess = bot.send_message(message.chat.id, unknownFuncMessage)
		show_main_options(message)



bot.infinity_polling()