import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# Абсолютные импорты
from bot.handlers.start import handle_start
from bot.handlers.products import handle_products
from bot.database.db import init_db
from config.settings import settings

# Инициализация логгера
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
    """Основная функция запуска бота"""
    try:
        logger.info("Starting bot initialization...")

        application = (
            ApplicationBuilder()
            .token(settings.BOT_TOKEN)
            .post_init(init_app)
            .build()
        )

        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", handle_start))
        application.add_handler(CommandHandler("products", handle_products))

        logger.info("Bot started. Press Ctrl+C to stop")
        application.run_polling()

    except Exception as e:
        logger.exception(f"Bot crashed: {e}")


if __name__ == '__main__':
    main()