from telegram import Update
from telegram.ext import ContextTypes
from bot.database.db import get_db
from bot.database.models import Product


async def handle_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = next(get_db())
    products = db.query(Product).all()

    if not products:
        await update.message.reply_text("Товары отсутствуют 😢")
        return

    response = "🔧 Доступные цилиндры:\n\n"
    for product in products:
        response += f"• {product.name} - {product.price} руб.\n"

    await update.message.reply_text(response)