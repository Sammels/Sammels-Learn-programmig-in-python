"""
Webapp 2 - Blueprints
"""
from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate


from webapp2.db import db
from webapp2.admin.views import blueprint as admin_blueprint
from webapp2.news.views import blueprint as news_blueprint
from webapp2.user.models import User
from webapp2.user.views import blueprint as user_blueprint

"""
Простейшее Flask приложение
Версия 3.

1. Добавление работы с HTML.
2. Созданы переменные weather
3. Добавлен index.html для фронта
"""


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    # Добавление миграции
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    
    # Регистрация БП
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
