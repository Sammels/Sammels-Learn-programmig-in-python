"""
Идет работа с Blueprints

"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Импорт дб из модел
from webapp2.db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))

    def set_password(self, password):
        # Исп. generate_password_hash для генерации хеша.
        self.password = generate_password_hash(password)


    def check_password(self, password):
        # Проверяем введеный хеш, и пароль в базе
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin' and self.is_active

    def __repr__(self):
        return "<User name={} id={}>".format(self.username,self.id)
