# Реализация обновления пользователя.

from db import db_session
from models import User

# Чтобы обновить данные, нужно получить пользователя
user = User.query.first()
# Изменение
user.salary = 59939
# Применение изменения
db_session.commit()
