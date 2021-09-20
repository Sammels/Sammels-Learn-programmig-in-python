from flask import Flask, render_template
from weather2 import weather_by_city
from python_org_news import get_python_news
"""
Простейшее Flask приложение
Версия 2.

1. Добавление работы с HTML.
2. Созданы переменные weather
3. Добавлен index.html для фронта


"""


app = Flask(__name__)


@app.route('/')
def index() -> str:
    page_title = "Новости Python"
    weather = weather_by_city("Bryansk,Russia")
    news_list = get_python_news()
    return render_template('index.html', title=page_title,
                           weather=weather, news_list=news_list)


if __name__ == "__main__":
    app.run(debug=True)
