# Импорт модели табл.
from sqlalchemy import Column, Integer, String
from db import Base, engine


class User(Base):
    # Создание таблицы
    __tablename__ = "users"

    # Создание колонок

    # id с целым числом и первичным ключом
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Integer)
    # String(120) - Макс длина строки, unique - уникальный
    email = Column(String(120), unique=True)

    
    def __repr__(self) -> str:
        return f"User {self.id}, {self.name}"

if __name__ == "__main__":
    # создает таблицу
    Base.metadata.create_all(bind=engine)