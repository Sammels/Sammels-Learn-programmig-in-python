# Рефакторинг кода
1. Разделить все по папкам.
2. Запускаемый скрипт переименовать из `server2.py` в `__init__.py`

Файлы с именем `__init__`.py автоматически исполняются при импорте модуля.

## Применим паттерн Фабрика
Фабрика - функция которая инициализзирует объект приложения фласка.

## Изменение процесса запуска приложения

`Linux + Mac`: ```export FLASK_APP=webapp && export FLASK_ENV=development && flask run```

`Windows`: `set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run`

# Рефакторинг кода `Добавление файла конфигурации`
1. Создаем новый файл `config.py`
`NAME_IN_CAPS = Константа`

2. Добавляем в главный скрипт `app.config.from_pyfile('config filename')`
3. Далее используем данные конфика как список
```python
weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
```
4. в weather2 добавить `from flask import current_app`
Данная конструкция позволяет обращатся к текущему фласк приложению.

5. Выносим URL так же в конфиг файл.

# Работа с БД исп SQLAlchemy
Исп. `flask-SQLAlchemy` 
уст. библ.
pip3 install flask-sqlalchemy

## Конфигурация
- Необходимо задать путь к sqlite - базе. Flask-SQLAlchemy исп для этого параметр
в конфигурации по ключу `SQLALCHEMY_DATABASE_URI`

- Необходимо задать путь к файлу не прописывая его в ручную
В конфиг файле в создадим путь
```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
```

Для работы с sqlite необходимо устрановить sqlite browser
`https://sqlitebrowser.org/dl/`

```
Debian

Note that Debian focuses more on stability rather than newest features. Therefore packages will typically contain some older version, compared to the latest release.

Update the cache using:

sudo apt-get update

Install the package using:

sudo apt-get install sqlitebrowser

```

## Модель News
Модель описывает объект который мы хотим сохранить в БД и получать из БД.
`SQLAlchemy` будет делать всю работу.
<p>Для работы с БД, нам нужно описать <b>модель</b>. Модель это описание объектов
которые мы хотим сохранять в БД и получать из неё</p>

1. Создать `model.py`

2. Записать этот код:
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

В файле `model.py` опишем модель:

```python
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    url = db.Column(db.String, unique=True, nullable=False)
    publushed = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<News {} {}'.formaat(self.title, self.url)

```

## Привязка баз к приложению Flask

В файле `__init__.py` добавим импорт
```python
from webapp.model import db
```
А в функцию create_app() строку
`db.init_app(app)`

## Создание БД
`SQLAlchemy` сама создаст файл бд, (если его ещё нет)

Создадим файл `create_db.py` в корне проекта

```python
from webapp import db, create_app

db.create_all(app=create_app())
``` 

## Перепишем get_python_news()
Проверим, что в `published` действительно лежат дата.

```python
from datetime import datetime

published = news.find('time').text
try:
    published = datetime.striptime(publushed, '%Y=%m-%d')
except(ValueError):
    published = datetime.now()
```

## Добавим функциб для записи новости в БД

Код ниже добавляется в `python_org_news.py`

```python
from webapp.model import db, News

...
def save_news(title, url, published):
    new_news = News(title=title, url=url, published=published)
    db.session.add(new_news)
    db.session.commit()

```

## Создадим файл, с помощью которогр мы будем собирать новости

Чтобы использовать `flask-sqlalchemy` не из flask приложения, нам придется
сделать несколько дополнительных действий.

1. Создаем в корне проекта файл `get_all_news.py`

```python
from webapp import create_app
from webapp.python_org_news import get_python_news

app = create_app()
with app.app_context():
    get_python_news()
```

2. Запуск проверка файла

Запуск `python_get_all_news.py` и проверка через SqlliteBrowser

3. Защита от ошибок.
При повторном запуске будет `sqlalchemy.exc.IntegrityError`

```python
def save_news(title, url, publushed):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()
```

