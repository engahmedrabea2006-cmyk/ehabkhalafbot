# تثبيت المكتبة (يفضل يكون في replit packages مش في الكود نفسه)
# os.system("pip install pyTelegramBotAPI")  ← شيلها

import os
from flask import Flask
from threading import Thread
import telebot

# ✅ التوكن بتاع البوت
BOT_TOKEN = "8282374430:AAGuJB5OizZeSyXqQUJ0t0CAh-o9M430FhM"
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ المسارات الخاصة بالفولدرات
short_path = "تلاوات قصيرة"
full_path = "سور كاملة"

# ✅ القائمة الرئيسية
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("▶️ تلاوات قصيرة", "📖 سور كاملة")
    return markup

# ✅ التعامل مع /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "أهلًا بك! اختر نوع التلاوة:", reply_markup=main_menu())

# ✅ قائمة التلاوات القصيرة
@bot.message_handler(func=lambda msg: msg.text == "▶️ تلاوات قصيرة")
def short_recitations(message):
    files = os.listdir(short_path)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for file in files:
        markup.row(f"📎 قصيرة: {file}")
    markup.row("🔙 رجوع")
    bot.send_message(message.chat.id, "اختر تلاوة قصيرة:", reply_markup=markup)

# ✅ قائمة السور الكاملة
@bot.message_handler(func=lambda msg: msg.text == "📖 سور كاملة")
def full_surahs(message):
    files = os.listdir(full_path)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for file in files:
        markup.row(f"📎 كاملة: {file}")
    markup.row("🔙 رجوع")
    bot.send_message(message.chat.id, "اختر سور كاملة:", reply_markup=markup)

# ✅ إرسال التلاوة القصيرة
@bot.message_handler(func=lambda msg: msg.text.startswith("📎 قصيرة:"))
def send_short_audio(message):
    file_name = message.text.replace("📎 قصيرة: ", "")
    with open(os.path.join(short_path, file_name), "rb") as audio:
        bot.send_audio(message.chat.id, audio)

# ✅ إرسال السور الكاملة
@bot.message_handler(func=lambda msg: msg.text.startswith("📎 كاملة:"))
def send_full_audio(message):
    file_name = message.text.replace("📎 كاملة: ", "")
    with open(os.path.join(full_path, file_name), "rb") as audio:
        bot.send_audio(message.chat.id, audio)

# ✅ الرجوع للقائمة الرئيسية
@bot.message_handler(func=lambda msg: msg.text == "🔙 رجوع")
def back(message):
    bot.send_message(message.chat.id, "رجعت للقائمة الرئيسية:", reply_markup=main_menu())

# ✅ Flask Server for UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ✅ تشغيل السيرفر ثم البوت
if __name__ == "__main__":
    print("✅ Flask server is running...")
    keep_alive()
    print("🤖 Telegram bot is polling...")
    bot.infinity_polling()
