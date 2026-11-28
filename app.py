import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# 1. BotFather'dan olgan tokeningizni shu yerga yozasiz
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZNI_SHU_YERGA_YOZING"

# 2. Adminlar ID'lari (1-raqam sizniki, 2-raqam ustozingizniki)
# O'zingiz va ustozingizning ID'sini @userinfobot orqali bilib olib, shu yerga yozasiz
ADMIN_IDS = [123456789, 987654321]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Start komandasi (skrinshotdagi ko'rinish)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    # Agar bu siz yoki ustozingiz bo'lsangiz, maxsus xabar chiqarish mumkin
    admin_status = "👑 Admin (To'liq huquq)" if user_id in ADMIN_IDS else "Foydalanuvchi"
    
    text = (
        f"Assalomu alaykum, {user_name}!\n"
        f" status: {admin_status}\n\n"
        f"✅ Obuna faol. Quyidan kerakli test darchasini tanlang:\n\n"
        f"• 🔓 <b>Demo:</b> 1- va 2-bo'limdan 1-mavzu, 3-bo'limdan 3 ta variant ochiq.\n"
        f"• 💎 <b>Premium:</b> Barcha mavzular va 70 ta variant to'liq ochiq!\n\n"
        f"🌟 <b>Premium foydalanish uchun:</b>\n"
        f"📌 Yopiq guruh, yangi demo testlar va video yechimlar\n"
        f"💳 To'lov: <b>69 900 so'm</b> (1 yilga amal qiladi)\n"
        f"📱 Murojaat uchun: <b>@dilshodtura1985</b>"
    )

    # Skrinshotdagi kabi inline tugmalar
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    demo_button = InlineKeyboardButton(
        "🔓 Demo test darchasini ochish", 
        callback_data="open_demo"
    )
    
    # Vercel'dagi saytingiz havolasini shu yerga qo'yasiz
    premium_button = InlineKeyboardButton(
        "💎 Premium test darchasini ochish (To'liq)", 
        url="https://iqtisodiyot-attestatsiya-uz.vercel.app/"
    )
    
    keyboard.add(demo_button, premium_button)

    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


# Misol: Faqat siz va ustozingiz kira oladigan maxsus admin buyruqi (/admin)
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
    from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') # templates papkasidagi index.html ni ochadi

if __name__ == '__main__':
    app.run(debug=True)