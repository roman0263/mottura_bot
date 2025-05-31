from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

# Путь к БД (создается в папке проекта)
DB_PATH = os.path.join(os.path.dirname(__file__), '../bot_data.sqlite')

engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()