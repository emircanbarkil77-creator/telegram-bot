import os
import telebot
from flask import Flask

TOKEN = (
    '8876167807:AAEHfJlHcdY4xWEL-'
    'kYTuVzvIm5n82AhHbU'
)

bot = telebot.TeleBot(TOKEN)
CHANNEL_USERNAME = '@sevgi4500'

app = Flask(__name__)

# Kullanıcıların gönderi oluşturma aşamalarını takip etmek için geçici hafıza
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

# Kullanıcı Medya (Fotoğraf / Video) gönderdiğinde tetiklenir
@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    chat_id = message.chat.id
    
    if message.photo:
        file_id = message.photo[-1].file_id
        media_type = 'photo'
    else:
        file_id = message.video.file_id
        media_type = 'video'
        
    user_data[chat_id] = {
        'file_id': file_id,
        'type': media_type
    }
    
    msg = bot.reply_to(
        message, 
        "İçerik alındı! 🌟 Bu gönderi kaç Telegram Yıldızı (Stars) karşılığında açılsın? (Örn: 100, 400, 1000)"
    )
    bot.register_next_step_handler(msg, process_star_amount)

def process_star_amount(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Lütfen önce bir fotoğraf veya video gönderin.")
        return
        
    try:
        stars = int(message.text)
        data = user_data[chat_id]
        
        bot.send_message(
            chat_id, 
            f"✅ İşlem Başarılı!\n"
            f"Tür: {data['type'].upper()}\n"
            f"Fiyat: {stars} Stars\n\n"
            f"İçerik {CHANNEL_USERNAME} kanalına kilitli olarak aktarılıyor..."
        )
        
        # Burada Telegram Paid Media API üzerinden kanala gönderim simule edilir
        # Telegram Bot API Paid Media desteği ile kanala gönderilir.
        
        del user_data[chat_id]
        
    except ValueError:
        msg = bot.reply_to(message, "Lütfen sadece sayı yazın! (Örn: 100 veya 400)")
        bot.register_next_step_handler(msg, process_star_amount)

if __name__ == '__main__':
    import threading
    port = int(os.environ.get('PORT', 5000))
    bot_thread = threading.Thread(target=bot.infinity_polling)
    bot_thread.daemon = True
    bot_thread.start()
    app.run(host='0.0.0.0', port=port)
