from telegram import Update
from telegram.ext import ContextTypes

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот для продажи цилиндров Mottura.",
        reply_markup=None
    )
