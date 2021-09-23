# Реализация добавления записи в БД

from db import db_session
from models import User
# Создать объект пользователя
first_user = User(name='Али-Баба Зухра', salary=9990, email='ArabNews@exampl.com')
# Использование сессии
db_session.add(first_user)
# Добавление записи в бд
db_session.commit()
