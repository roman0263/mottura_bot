import csv
from sqlalchemy.orm import Session
from bot.database.models import Product

class ProductRepository:
    # ... существующие методы ...

    @staticmethod
    def import_from_csv(db: Session, file_path: str):
        """Импорт товаров из CSV файла"""
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