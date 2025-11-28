from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = "8204695273:AAFsodphzWnC9TbEhMN3_-A9mWIoE12ukKY"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def reply(update, context):
    user_text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}],
    )

    bot_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(bot_reply)

updater = Updater(BOT_TOKEN, use_context=True)
handler = MessageHandler(Filters.text & (~Filters.command), reply)
updater.dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()
