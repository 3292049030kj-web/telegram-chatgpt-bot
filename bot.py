import os
import logging
import asyncio
import openai

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler, ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Missing BOT_TOKEN or OPENAI_API_KEY environment variables.")

# OpenAI 新版 API 初始化
openai.api_key = OPENAI_API_KEY


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=200,
        )
        bot_reply = resp["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.error("OpenAI request failed: %s", e)
        bot_reply = "Error contacting OpenAI."

    await update.message.reply_text(bot_reply)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

    logger.info("Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
