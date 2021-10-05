from flask import Flask, render_template


from webapp.model import db, News
from weather2 import weather_by_city
"""
Простейшее Flask приложение
Версия 2.

1. Добавление работы с HTML.
2. Созданы переменные weather
3. Добавлен index.html для фронта
"""


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index() -> str:
        page_title = "Новости Python"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', title=page_title,
                               weather=weather, news_list=news_list)

    return app
