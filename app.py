import os
import threading
import logging
from flask import Flask, render_template
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Token va Adminlar
BOT_TOKEN = "9290641376:AAG_TYekifqmDD492uyl4j9r3-CAbCrT18Y"
ADMIN_IDS = [8990585770, 987654321]

# Bot va Flask sozlamalari
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

# --- TELEGRAM BOT QISMI ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    admin_status = "👑 Admin (To'liq huquq)" if user_id in ADMIN_IDS else "Foydalanuvchi"
    
    text = (
        f"Assalomu alaykum, {user_name}!\n"
        f"status: {admin_status}\n\n"
        f"✅ Obuna faol. Quyidan kerakli test darchasini tanlang:\n\n"
        f"• 🔓 <b>Demo:</b> 1- va 2-bo'limdan 1-mavzu, 3-bo'limdan 3 ta variant ochiq.\n"
        f"• 💎 <b>Premium:</b> Barcha mavzular va 70 ta variant to'liq ochiq!\n\n"
        f"🌟 <b>Premium foydalanish uchun:</b>\n"
        f"📌 Yopiq guruh, yangi demo testlar va video yechimlar\n"
        f"💳 To'lov: <b>69 900 so'm</b> (1 yilga amal qiladi)\n"
        f"📱 Murojaat uchun: <b>@dilshodtura1985</b>"
    )

    keyboard = InlineKeyboardMarkup(row_width=1)
    demo_button = InlineKeyboardButton("🔓 Demo test darchasini ochish", callback_data="open_demo")
    premium_button = InlineKeyboardButton("💎 Premium test darchasini ochish (To'liq)", url="https://iqtisodiyot-attestatsiya-uz.vercel.app/")
    keyboard.add(demo_button, premium_button)

    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.reply(
            "👨‍💻 <b>Admin panelga xush kelibsiz!</b>\n\n"
            "• To'lov qilgan foydalanuvchilarni sayt kodiga qo'shish uchun:\n"
            "<i>index.html</i> faylidagi <code>PREMIUM_FOYDALANUVCHILAR</code> ro'yxatiga uning nikini yozib, Vercel'ga yangilaysiz.",
            parse_mode="HTML"
        )
    else:
        await message.reply("Sizda bu buyruqdan foydalanish huquqi yo'q.")


def run_bot():
    # Botni alohida oqimda (background thread) yurgazamiz
    executor.start_polling(dp, skip_updates=True)


# --- FLASK (WEB SAYT) QISMI ---
@app.route('/')
def home():
    # index.html fayli 'templates' papkasi ichida turishi shart!
    return render_template('index.html')


if __name__ == '__main__':
    # 1. Telegram bot uchun alohida oqim ochamiz
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # 2. Flask serverini ishga tushiramiz (Hostinglar talab qiladigan PORT bilan)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)