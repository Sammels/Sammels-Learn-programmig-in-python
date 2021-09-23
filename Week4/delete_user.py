# Удаление пользователя
from db import db_session
from models import User

# Получаем первого пользователя
user = User.query.first()
# Сессия на удаление
db_session.delete(user)
# Отправка запроса в БД 
db_session.commit()