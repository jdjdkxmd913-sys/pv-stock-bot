import os
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types

# Токен із змінних Railway
TOKEN = os.getenv("TELEGRAM_TOKEN")  
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

subscribers = set()
URL = "https://plantsvsbrainrots.com/stock"

# Функція перевірки сайту
def check_site():
    try:
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        stock = soup.get_text(strip=True)
        return stock
    except Exception as e:
        return f"❌ Помилка: {e}"

# /start – підписка на оновлення
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    subscribers.add(message.chat.id)
    await message.answer("✅ Ви підписалися на оновлення стоку!")

# Періодична перевірка сайту
async def stock_checker():
    last_stock = ""
    while True:
        current_stock = check_site()
        if current_stock != last_stock and current_stock != "":
            last_stock = current_stock
            for user in subscribers:
                try:
                    await bot.send_message(user, f"🔄 Новий сток:\n{current_stock}")
                except Exception:
                    pass
        await asyncio.sleep(320)  # кожні 5 хвилин і 20 секунд

# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(stock_checker())
    executor.start_polling(dp, skip_updates=True)
