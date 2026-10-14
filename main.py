import telebot

TOKEN = '8876167807:AAEHfJlHcdY4xWEL-kYTuVzvIm5n82AhHbU
bot = telebot.TeleBot(TOKEN)
CHANNEL_USERNAME = '@sevgi4500'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Paid Media (100 Stars) botu aktif ve çalışıyor.")

@bot.message_handler(commands=['paylas'])
def send_paid_media_post(message):
    try:
        bot.send_message(message.chat.id, "Paid media içeriği @sevgi4500 kanalına gönderiliyor...")
        bot.send_message(CHANNEL_USERNAME, "Bu mesaj 100 Stars (Paid Media) ile gönderilmiştir.")
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")

if __name__ == '__main__':
    print("Bot çalışıyor...")
    bot.infinity_polling()
