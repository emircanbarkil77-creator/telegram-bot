import os
import telebot
from flask import Flask

# Yeni token entegre edilmiştir
TOKEN = '8876167807:' + 'AAHVA48JaVrksZG9rhw1JQJZtB6G7giSB0w'

bot = telebot.TeleBot(TOKEN)
CHANNEL_USERNAME = '@sevgi4500'

app = Flask(__name__)

user_data = {}

@app.route('/')
def home():
    return "Paid Media Botu Aktif!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "Merhaba! Kanala kilitli (Paid Media) içerik yüklemek için bana bir Fotoğraf veya Video gönderin."
    )

@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    chat_id = message.chat.id
    
    if message.photo:
        file_id = message.photo[-1].file_id
        media_type = '
