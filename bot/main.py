import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
from dotenv import load_dotenv
import os
from .database import db
from .handlers import start, products

# Загрузка переменных окружения
load_dotenv()

# Инициализация логгера
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def init(application):
    """Инициализация при запуске"""
    await application.bot.set_my_commands([
        ('start', 'Запустить бота'),
        ('products', 'Список товаров')
    ])
    db.init_db()  # Создаем таблицы в БД
    logging.info("Database initialized")


def main():
    # Создаем приложение бота
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).post_init(init).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start.handle_start))
    application.add_handler(CommandHandler("products", products.handle_products))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()