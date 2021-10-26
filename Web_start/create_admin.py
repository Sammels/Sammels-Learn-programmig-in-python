from getpass import getpass
import sys

from webapp import create_app
from webapp.model import User, db

app = create_app()

with app.app_context():
    # Запрашиваем имя пользователя в cmd
    username = input("Введите имя пользователя: ")
    # Проверка существует ли такой пользователь
    if User.query.filter(User.username == username).count():
        print("Такой пользователь уже есть")
        # Используя sys выходим из нашей программы
        sys.exit(0)

    password1 = getpass("Введите пароль: ")
    password2 = getpass("Повторите пароль: ")
    if not password1 == password2:
        print("Разные пароли")
        sys.exit(0)

    new_user = User(username=username, role="admin")
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print("Создан пользователь с id={}".format(new_user.id))
