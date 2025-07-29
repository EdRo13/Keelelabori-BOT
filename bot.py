
import os
import logging
from aiogram import Bot, Dispatcher, types, executor
import openai

# Настройки логов
logging.basicConfig(level=logging.INFO)

# Получение переменных из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment variables.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Инициализация бота и OpenAI
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        user_input = message.text

        # Обращение к OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Можно заменить на gpt-4, если доступно
            messages=[
                {"role": "system", "content": "Vasta ainult eesti keeles. Sa oled vestlusrobot, kes aitab inimestel harjutada eesti keelt."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message["content"]
        await message.reply(reply)

    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await message.reply("Vabandust, tekkis tehniline probleem.")

if __name__ == "__main__":
    logging.info("Bot polling started")
    executor.start_polling(dp, skip_updates=True)
