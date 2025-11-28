import os
import logging
from telegram.ext import Updater, MessageHandler, Filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Missing BOT_TOKEN or OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def reply(update, context):
    user_text = update.message.text or ""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        logger.exception("OpenAI error")
        bot_reply = "OpenAI API 调用失败：" + str(e)

    update.message.reply_text(bot_reply)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), reply))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
