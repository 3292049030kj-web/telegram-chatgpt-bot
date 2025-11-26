import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

# Load tokens from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
client = OpenAI(api_key=OPENAI_API_KEY)


@dp.message_handler()
async def chatgpt_reply(message: types.Message):
    """Reply to Telegram users with ChatGPT response"""
    try:
        user_text = message.text

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )

        answer = response.choices[0].message["content"]
        await message.answer(answer)

    except Exception as e:
        print("Error:", e)
        await message.answer("⚠️ Error, please check the bot logs.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
