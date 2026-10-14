import os
import requests
import telebot
from flask import Flask

TOKEN = os.environ.get('BOT_TOKEN')
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
        
        # Telegram API'ye doğrudan istek atarak kesin kilitli (paid media) gönderiyoruz
        url = f"https://api.telegram.org/bot{TOKEN}/sendPaidMedia"
        
        payload = {
            "chat_id": CHANNEL_USERNAME,
            "star_count": stars,
            "media": [
                {
                    "type": data['type'],
                    "media": data['file_id'],
                    "caption": f"🔓 Bu içeriği açmak için {stars} Stars ödeyin."
                }
            ]
        }
        
        response = requests.post(url, json=payload)
        print("Telegram API Yanıtı:", response.text)
            
        del user_data[chat_id]
        
    except ValueError:
        msg = bot.reply_to(message, "Lütfen sadece sayı yazın! (Örn: 100, 400 veya 1000)")
        bot.register_next_step_handler(msg, process_star_amount)

if __name__ == '__main__':
    import threading
    port = int(os.environ.get('PORT', 5000))
    bot_thread = threading.Thread(target=bot.infinity_polling)
    bot_thread.daemon = True
    bot_thread.start()
    app.run(host='0.0.0.0', port=port)
