"""
Работа с блюпринтами
"""
from flask import Blueprint, current_app, render_template

from webapp2.news.models import News
from weather2 import weather_by_city


# Основной роутинг. Префикса не будет
blueprint = Blueprint("news", __name__)


@blueprint.route("/")
def index() -> str:
    page_title = "Новости Python"
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template(
        "news/index.html", title=page_title, weather=weather, news_list=news_list
    )
