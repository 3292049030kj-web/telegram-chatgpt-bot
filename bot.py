import os
import logging
import asyncio
import openai

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Missing BOT_TOKEN or OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)   # GPT-4o mini 新接口


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个中文助手，所有回答都使用中文。"},
                {"role": "user", "content": user_text},
            ],
            max_tokens=200,
        )

        bot_reply = completion.choices[0].message["content"].strip()

    except Exception as e:
        logger.error(f"OpenAI failed: {e}")
        bot_reply = "调用 GPT 失败，请稍后再试。"

    await update.message.reply_text(bot_reply)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    logger.info("Bot started…")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
