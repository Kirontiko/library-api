import logging
import os
import django
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def set_user_chat_id_async(token, chat_id):
    User = get_user_model()
    get_user = sync_to_async(User.objects.get)
    user = await get_user(token=token)
    user.chat_id = chat_id
    await sync_to_async(user.save)()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    token = update.effective_message.text.split()[-1]
    await set_user_chat_id_async(token, chat_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome to Library API 🤓📚"
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
