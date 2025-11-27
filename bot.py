import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI

BOT_TOKEN = 8204695273:AAFsodphzWnC9TbEhMN3_-A9mWIoE12ukKY("BOT_TOKEN")
OPENAI_API_KEY =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("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_text}
        ],
    )

    bot_reply = response.choices[0].message.content
    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

app.run_polling()
