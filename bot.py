import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from openai import OpenAI

# 从 Render 环境变量获取 Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 创建 Telegram bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# 创建 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await message.reply("🤖 你好！我是你的 ChatGPT 机器人。\n请发送任何消息，我会回复你。")

@dp.message_handler()
async def chat_handler(message: types.Message):
    user_text = message.text

    try:
        # 调用 OpenAI Chat Completion (新 API)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_text}
            ]
        )

        reply_text = response.choices[0].message.content
        await message.reply(reply_text)

    except Exception as e:
        await message.reply("⚠️ 出错了：" + str(e))
        print("OpenAI 错误：", e)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
