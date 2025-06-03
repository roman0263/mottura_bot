import csv
from sqlalchemy.orm import Session
from bot.database.models import Product

class ProductRepository:
    @staticmethod
    def import_from_csv(db: Session, file_path: str):
        """Импорт товаров из CSV"""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = Product(
                        name=row['name'],
                        description=row.get('description', ''),
                        price=float(row['price']),
                        category=row.get('category', 'other')
                    )
                    db.add(product)
                db.commit()
                return True, "Товары успешно импортированы"
        except Exception as e:
            db.rollback()
            return False, f"Ошибка: {str(e)}"