import os
import logging
from telegram.ext import Updater, MessageHandler, Filters
import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    logger.error("Missing BOT_TOKEN or OPENAI_API_KEY environment variables.")
    raise RuntimeError("Set BOT_TOKEN and OPENAI_API_KEY in environment variables.")

openai.api_key = OPENAI_API_KEY


def reply(update, context):
    user_text = update.message.text or ""

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=200,
        )
        bot_reply = resp['choices'][0]['message']['content'].strip()

    except Exception as e:
        logger.exception("OpenAI request failed")
        bot_reply = "Error contacting OpenAI: " + str(e)

    update.message.reply_text(bot_reply)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), reply))

    logger.info("Bot started polling...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
