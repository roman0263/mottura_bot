from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings  # Используем централизованные настройки

Base = declarative_base()

# Создаем движок с учетом настроек из config/settings.py
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=True  # Логирование SQL-запросов (можно отключить в продакшене)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Генератор сессий для Dependency Injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()