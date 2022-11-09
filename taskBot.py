import telebot

bot = telebot.TeleBot('5741260025:AAEUYgaP6f1ULfHe9gbsViVZ_XEJn0DjhGA')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Welcome, this is tasklist bot!")




bot.infinity_polling()