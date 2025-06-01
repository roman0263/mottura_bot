from telegram import Update
from telegram.ext import ContextTypes
from bot.database.db import SessionLocal  # Исправленный импорт
from bot.database.models import Product  # Импорт модели


async def handle_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as session:
        products = session.query(Product).all()

        if not products:
            await update.message.reply_text("Товары не найдены.")
            return

        response = "📦 Список товаров:\n\n"
        for product in products:
            response += f"• {product.name} - {product.price}₽\n"

        await update.message.reply_text(response)