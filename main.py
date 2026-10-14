import os
import telebot
from flask import Flask

# Parantez yöntemiyle telefonda kayma/bölünme sorunu tamamen ortadan kalkar
TOKEN = (
    '8876167807:AAEHfJlHcdY4xWEL-'
    'kYTuVzvIm5n82AhHbU'
)

bot = telebot.TeleBot(TOKEN)
CHANNEL_USERNAME = '@sevgi4500'

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot aktif!")

if __name__ == '__main__':
    import threading
    port = int(os.environ.get('PORT', 5000))
    bot_thread = threading.Thread(target=bot.infinity_polling)
    bot_thread.daemon = True
    bot_thread.start()
    app.run(host='0.0.0.0', port=port)
