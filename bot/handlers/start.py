from telegram import Update
from telegram.ext import ContextTypes
from bot.database.db import SessionLocal
from bot.database.models import User


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    with SessionLocal() as session:
        db_user = session.query(User).filter(User.telegram_id == user.id).first()

        if not db_user:
            new_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            session.add(new_user)
            session.commit()
            await update.message.reply_text(f"Привет, {user.first_name}! Вы зарегистрированы.")
        else:
            await update.message.reply_text(f"С возвращением, {db_user.first_name}!")