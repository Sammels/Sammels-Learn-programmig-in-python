# Реализация получения данных из бд

from models import User
# Запрос на первого пользователя
user = User.query.first()
print(f"""Имя {user.name}
Зарплата {user.salary}
Email {user.email}
""")
