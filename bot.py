import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "7981937789:AAFyKK0MgFHZeY0S9K5FyZa87RIGz-UZH8Y"  # এখানে আপনার টোকেন বসান

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ইউজার ডেটা রাখার জন্য (ডেমোতে মেমরিতে, আসল প্রজেক্টে DB লাগবে)
users = {}
ads_link = "https://example.com"  # এখানে আপনার এড লিঙ্ক দিন

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {"coins": 0}
    await message.answer(
        "👋 স্বাগতম!\n\n💰 এড দেখে কয়েন আয় করুন!\n\n"
        "/watch - এড দেখুন\n"
        "/balance - ব্যালান্স দেখুন\n"
        "/withdraw - উইথড্র রিকোয়েস্ট দিন"
    )

@dp.message_handler(commands=['watch'])
async def watch_ads(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {"coins": 0}
    users[uid]["coins"] += 1  # প্রতিবার এড দেখলে ১ কয়েন
    await message.answer(f"👉 আপনার এড: {ads_link}\n\n✅ আপনি ১ কয়েন পেলেন!")

@dp.message_handler(commands=['balance'])
async def check_balance(message: types.Message):
    uid = message.from_user.id
    coins = users.get(uid, {"coins": 0})["coins"]
    await message.answer(f"💰 আপনার ব্যালান্স: {coins} কয়েন")

@dp.message_handler(commands=['withdraw'])
async def withdraw(message: types.Message):
    uid = message.from_user.id
    coins = users.get(uid, {"coins": 0})["coins"]
    if coins >= 10:  # মিনিমাম ১০ কয়েন
        users[uid]["coins"] = 0
        await message.answer("✅ আপনার উইথড্র রিকোয়েস্ট অ্যাডমিনের কাছে পাঠানো হয়েছে।")
    else:
        await message.answer("❌ মিনিমাম ১০ কয়েন লাগবে উইথড্র করার জন্য।")

# --- শুধুমাত্র অ্যাডমিনের জন্য (এড লিঙ্ক আপডেট) ---
ADMIN_ID = 7097753085  # এখানে আপনার Telegram ID বসান

@dp.message_handler(commands=['setad'])
async def set_ad(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        global ads_link
        parts = message.text.split(" ", 1)
        if len(parts) > 1:
            ads_link = parts[1]
            await message.answer(f"✅ নতুন এড লিঙ্ক সেট হয়েছে:\n{ads_link}")
        else:
            await message.answer("⚠️ ব্যবহার: /setad LINK")
    else:
        await message.answer("❌ এই কমান্ড শুধু অ্যাডমিন ব্যবহার করতে পারবে।")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
