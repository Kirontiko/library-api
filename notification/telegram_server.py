import logging
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    print(update.effective_chat.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome to Library API 🤓📚"
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(os.environ["TELEGRAM_TOKEN"])
        .build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
