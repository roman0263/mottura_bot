import logging
import os
import tempfile
from telegram import Update, Document
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters
)

# Абсолютные импорты
from bot.handlers.start import handle_start
from bot.handlers.products import handle_products
from bot.database.db import init_db, SessionLocal
from config.settings import settings
from bot.database.repository import ProductRepository

# --- Админские обработчики ---

async def handle_import(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /import — импорт из CSV по пути на сервере"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    try:
        chat_admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in chat_admins]
    except Exception:
        admin_ids = [settings.ADMIN_ID]

    if user_id not in admin_ids:
        await update.message.reply_text("❌ Доступ запрещён. Только администраторы.")
        return

    if not context.args:
        await update.message.reply_text("ℹ️ Использование: /import путь/к/файлу.csv")
        return

    csv_path = context.args[0]

    if not os.path.isfile(csv_path):
        await update.message.reply_text(f"❌ Файл не найден: {csv_path}")
        return

    try:
        with SessionLocal() as session:
            success, message = ProductRepository.import_from_csv(session, csv_path)
            await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при импорте: {e}")


async def handle_csv_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Загрузка CSV-файла в чат"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    try:
        chat_admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in chat_admins]
    except Exception:
        admin_ids = [settings.ADMIN_ID]

    if user_id not in admin_ids:
        await update.message.reply_text("⛔ Доступ запрещён. Только администраторы.")
        return

    document: Document = update.message.document

    if not document or not document.file_name.endswith('.csv'):
        await update.message.reply_text("❌ Отправьте файл с расширением `.csv`.")
        return

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, document.file_name)
        try:
            await document.get_file().download_to_drive(file_path)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка загрузки файла: {e}")
            return

        try:
            with SessionLocal() as session:
                success, message = ProductRepository.import_from_csv(session, file_path)
                await update.message.reply_text(message)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при импорте: {e}")


# --- Логгер ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)


async def init_app(application):
    """Инициализация при запуске"""
    try:
        await application.bot.set_my_commands([
            ('start', 'Запустить бота'),
            ('products', 'Список товаров')
        ])
        init_db()
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.critical(f"Initialization failed: {e}")
        raise


def main():
    """Запуск Telegram-бота"""
    try:
        logger.info("Starting bot initialization...")

        application = (
            ApplicationBuilder()
            .token(settings.BOT_TOKEN)
            .post_init(init_app)
            .build()
        )

        # Обработчики
        application.add_handler(CommandHandler("start", handle_start))
        application.add_handler(CommandHandler("products", handle_products))
        application.add_handler(CommandHandler("import", handle_import))
        application.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("csv"), handle_csv_upload))

        logger.info("Bot started. Press Ctrl+C to stop")
        application.run_polling()

    except Exception as e:
        logger.exception(f"Bot crashed: {e}")


if __name__ == '__main__':
    main()
