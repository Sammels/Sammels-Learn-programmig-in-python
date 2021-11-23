# Начало трека по Web программированию
Фреймворк выбирается под задачу

## Week 1

1. Простое веб-приложение на Flask
2. API и регистрация на сайте прогноза погоды
3. Получаем прогноз погоды при помощи requests
4. Добавляем прогноз погоды в веб-приложение
5. Слайды

## Week 2

## week 6 файлы в `webapp/`
1. Формы и пользователи
2. Как устроенны веб-формы
3. Создаем форму логина
4. Модель User
5. Создаем первого пользователя
6. Подключим Flask-login в приложении
7. Проверка прав доступа
8. Важные мелочи.



### 1. Формы пользователя
Управление зависимостями
Нужно создать файл `requirements.txt` можно так `pip3 freeze > requirements.txt`

Установка зависимостей
`pip3 install -r requirements.txt`

### 2. Как устроены веб формы
1. Создадим страницу с формой логина при помощи Flask-WTF
2. Создадим модель User и таблицу в базе данных
3. Создадим пользователя "Администратор"
4. Добавим функционал проверки логина/пароля при помощи Flask-Login
5. Создадим раздел, доступный только администраторам

Веб-формы (`w3schools.com`)- набор полей который заполняет пользователь в браузере и данные которых
передаются на сервер для дальнейшей обработки.

1. Сервер генерирует страницу с формой и отдает браузеру
2. Браузер рисует страницу и пользователь заполняет форму
3. Пользователь отправляет (submit) форму на определенный URL
4. Сервер обрабатывает пришедшие из формы данные.

### 3. Создаем Форму логина
1. Создадим файл forms.py с описанием формы

2. Опишем форму в виде объекта
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtform.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Отправить')

```
3. Открываем `__init__.py` и импортируем форму

`from webapp.forms import LoginForm`

```python
...
from webapp.forms import LoginForm
...

def create_app():
    ...

    @app.route('/login')
    def login():
        page_title = "Авторизация"
        # Нужно создать экземпляр формы (класс), некое формальное описание
        # чтобы работать с формой
        login_form = LoginForm()
        return render_template ('login.html', page_title=title, form=login_form )
...
```

4. В папке `templates` создаем `.html` login

```html
<form action="" method="post">
    {{ form.hidden_tag() }}
    <p>
        {{ form.username.label }} <br>
        {{ form.username() }}
    </p>
    <p>
        {{ form.password.label }}<br>
        {{ form.password() }}
    </p>
    <p>{{ form.submit }}</p>
</form>
```

5. Добавим в параметр SECRET_KEY в config
Переменная уонфигурации `SECRET_KEY` - Важная часть приложений Flask. Исп в кач-ве 
криптогрфич. ключа, при генерации подписей или токенов. Flask-WTF исп его для защиты веб-форм от csrf, xss, other.

6. Запуск сервера
linux и mac : `export FLASK_APP=webapp && export FLASK_ENV=development && flask run`

7. Используем верстку Bootstrap
Bootstrap дает удоные инструменты для реализации форм и кнопок

7.1. Добавим
```html
<div class="form-group">
            {{ form.username.label }}
            ...
          </div>
          <div class="form-group">
            {{ form.password.label }}
            ...
          </div>
```
7.2. Добавим css классы к полям
```python
...
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
...
```
`render_kw` - парамтр того, что будет добавлятся к полю когда оно рендериться.

### 4. Модель User
Модель пользователя

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def __repr__(self):
        return f'<User {self.username}>'


```

------
Создание таблицы в БД и установка Flask-Login
Flask-Login - Библиотека для удобной реализации процесса логина.
При этом библиотека не берет на себя вопросы проверка пароля, прав пользователя, регистрации и т.д.

`python3 create_db.py`

`pip3 install flask-login`

<b>Flask-Login</b>
flask-Login требует дополнительные атрибуты и методы в модели User
1. `is_authenticated`: True, если пользователь успешно авторизоваться иначе False
2. `is_active: True`: если учетная запись Пользователя активна, иначе False
3. `is_anonymous`: Flask-Login выставит это свойство в True, если пользователь не авторизирован.
4. `get_id()`: метод, который возвращает id пользователя в виде строки.

Добавим в модель интеграцию с Flask-Login

Исп. `UserMixin`

```python
from flask_login import UserMixin
...

class User(db.Model, UserMixin):
    ...

```

#### Научим модель работать с паролем

`Никогда нне храните пароль бд в открытом виде`

```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    ...

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)
...
```

#### Создаем пользователя
Напишем скрипт создания пользователей. `create_admin.py`

```python
from getpass import getpass
import sys

from webapp import create_app
from webapp.model import User, db

app = create_app()
```
Создадим пользователя

<b>Стадия 1: Проверки</b>

```python
with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password1 = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password1 == password2:
        sys.exit(0)
```

<b>Стадия 2: Создание пользователя</b>

```python
...
new_user = User(username=username, role='admin')
new_user.set_password(password)

db.session.add(new_user)
db.session.commit()
print('User with id {} added'.format(new_user.id))
```

### 6. Подключим Flask-Login в приложение
в `__init__.py`

```python
from flask_login import LoginManager
from webapp.model import db, News, User

def create_app():
    ...
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
```
Далее необходимо реализовать обработку формы логина

- Необходимо использоать `login_user` из `flask_login`

```python
from flask_login import LoginManager, login_user
```
- Реализуем несколько дополнительных функций из Flask

```python
from flask import Flask, render_template, flash, riderect, url_for
```

`flash` - позволяет передавать сообщения между route-ми
`redirect` - делает перенаправление на другую страницу пользователя.
`url_for` - помогает получить url по имени функции, которая этот url обрабатывает.

------
<b>Реализация обработки формы логина</b>

```python
...
@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))
...
```
<b>Доработаем форму логина</b>
Нужно передать данные формы на `/process-login`. Будем исп `url_for`

```html
<form action="{{ url_for('process_login') }}" method="post"
```
<b>Добавим в шаблоны отображение сообщений из flash</b>

```html
{% with messages = get_flashed_messages() %}
    {% if messages %}
    <div class="alert alert-warning" role="alert">
        {% for message in messages %}
            {{ message }}<br>
        {% endfor %}
    </div>
    {% endif %}
{% endwith %}
```

<b>Добавим возможность завершить сессию</b>

```python
from flask_login import LoginManager, login_user, logout_user

...
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```

### 7. Проверка прав доступа
#### Уберем возможность заходить на страницу /login для авторизированных

Если пользователь уже авторизирован и по какой-то причине зашел на /login - 
перенаправим его на главную:

```python
from flask_login import LoginManager, current_user, login_user, logout_user

...

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
```

#### Создадим страницу, доступную только зарегестрированным
```python
from flask_login import (LoginManager, current_user, login_required, Login_user, logout_user)
...

@app.route('/admin')
@login_required
def admin_index():
    return 'Привет админ!'
```

#### Класс должен сообщать нам, является ли пользователь администратором

Добавим в классе User метод `is_admin`. Декоратор `@property` позволяет вызывать метод как аттрибут, без скобочек:

```python
class User(db.Model, UserMixin):
...

    @property
    def is_admin(self):
        return self.role == 'admin' and self.is_active
    
```

## Week 7

1. Функционал "Запоминания" пользователя
2. Что такое Blueprint
3. Создадим первый Blueprint
4. Blueprint-ы для news и admin
5. Наследование шаблонов
6. Главное меню

<b>Запускать через /blueprint/target </b>

### 1. Функционал "Запоминания" пользователя

Если пользователь авторизуется и закроет браузер, то при следующем входе ему придется делать это снова. Нужно реализовать Функционал Запоминания пользователя.
Для этого в `forms.py` добавим поле:

```python
from wtforms import BooleanField, PasswordField, StringField, SubmitField

class LoginForm(FlaskForm):
    ...
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
```

В шаблоне `login.html` Добавим отображение нового поля:

```html
<div class="form-group form-check">
    {{ form.remember_me() }}
    {{ form.remember_me.label(class_='form-check-label') }}
</div>
```

В `__init__.py` в `process_login():` добавить

```python
...
if user and user.check_password(form.password.data):
    login_user(user, remember=form.remember_me.data)
```

Длительность соххранения статуса авторизации настраивается через конфигурацию Flask

```python
from datetime import timedelta

REMEMBER_COOKIE_DURATION = timedelta(days=5)
```

### 2. Что такое Blueprint? (Выполнено в webapp2.)

`Blueprint` - стандартный метод разделения Flask-приложения на модули. Они помогают разбить большое приложение на несколько функциональных модулей и поддерживать удобную структуру именования URL

1 из важных задач программиста, борьба со сложностью.
Во Фласке модуль называется в ед.ч. Наполнение во множественном числе.


Важно организовать код таким образом, чтобы в нем было легко разобраться,

<b>Как будет устроено приложение.</b>

Уже сейчас инит перегружен роутами. Выделение на модули

1. `news` - Страница новостей
2. `user` - Авторизация, регистрация, профиль пользователя
3. `admin` - админка, для управления контентом, и пользователями.

```
webapp/
    __init__.py
    config.py
    db.py
    user/
        __init__.py
        forms.py
        models.py
        views.py
    templates/
        base.html
        user/
            login.html
            registration.html
```
Начало с `user` - там больше всего функционала. `__init__.py` пустой, будет говорить питону, что это модуль.
`forms.py` - Формы для работы с пользователями.
`models.py` - Модель Юзера
`views.py` - Роуты которые относятся к user. Возможность для дальнейшего.

`templates` - где логин, индекс
`base.html` - Шаблон, который будет отвечать за базувую верстку. Одинаковый код будет перенесен в базовый шаблон, все остальные шаблоны будут от него наследовать.
В templates будет `название blueprinta`  относящиеся к нему.
`login.html`
`regostration.html`


Кроме `user` будет blueprint `admin`.

Благодаря стандартизации будет все достаточно легко понять.

### 3. Создадим первый Blueprint

`Каждый blueprint находится в отдельной папке.`

1. Создадим `user` а в ней файлы: `__init__.py, forms.py, models.py, views.py`  - Done

2. В `forms.py` перенесем код формы логина и удалим файл `forms.py` в корне приложения.
В `models.py` перенесем код модели User


В `views.py` пеенесем login(), progress_login(), logout(), в начало добавим код:

```python
from flask import Blueprint

blueprint = Blueprint('user', __name__m url_prefix='/users')
```

Так же нужно будет пройти по коду и поменять `url_for('login')` на `url_for('user.login')` и поправить import.

Теперь надо пройти по коду и поменять 
`@app.route` на  `@blueprint.route`
`url_for('login')` на `url_for('user.login')`

Готовый blueprint подключается в приложение:

```python
from webapp2.user.views import blueprint as user_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    app.register_blueprint(user_blueprint)

...

@blueprint.route("/logout")
def logout():
    # Реализация окончание сессии
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("news.index"))
```

### 4 - Blueprint-ы для news и admin
- В папке `webapp2` создаем папку `admin` в неё кладем `__init__.py` 
- В папке `webapp2/admin` создаем `views.py` и добавляем:

```python
from flask import Blueprint
from flask_login import current_user, login_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@login_required
def admin_index():
    if current_user.is_admin:
        return "Привет админ"
    else:
        return "Ты не админ"
```

- В `webapp2/__init__.py` добавить
```python
...
from webapp2.admin.views import blueprint as admin_blueprint
...
def create_app():
    ...
    # Регистрация БП
    ...

    app.register_blueprint(admin_blueprint)
```

В `webapp2/news` создаем `__init__.py`, `models.py`, `views.py`

- В `news/models.py` переносим из `webapp2 models.py`
```python
from webapp2.model import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return "<News {} {}".format(self.title, self.url)

```

- В `news/views.py`
```python
"""
Работа с блюпринтами
"""
from flask import Blueprint, current_app, render_template

from webapp2.news.models import News
from weather2 import weather_by_city


# Основной роутинг. Префикса не будет
blueprint = Blueprint('news', __name__)

@blueprint.route("/")
def index() -> str:
    page_title = "Новости Python"
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template(
        "index.html", title=page_title, weather=weather, news_list=news_list
    )


```
- в `webapp2/__init__.py` добавляется 

```python
from webapp2.news.views import blueprint as news_blueprint
...

def create_app():
    ...
    app.register_blueprint(news_blueprint)
```

- Если в друг все в одной папке то 
```python
from getpass import getpass
import sys

from webapp2 import create_app
from webapp2.db import db
from webapp2.news.models import User

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

```

### 5 - Наследование шаблонов
В шаблонах много повторяющегося кода. Его нужно вынести в шаблон `base.html` и все остальные шаблоны будут содержать только специфичный для данного шаблона.

- Создаем `base.html` из `index.html`

```html
  <div class="container">
    <h1>{{ title }}</h1>
    {% block content %}
    {% endblock %}

  </div>
```
За основу возмем наш index.html и вместо контентной части шаблона напишем
```
{% block content %}
{% endcontent %}
```
- Контент страницы пока скопируем в отдельный файл, назовем его `index.html` и сохраним в `templates/news/`

<b>Поменяем шаблон главной страницы</b>
В шаблоне index.html заключим `<div class="row">...</div>` в код `{% block content %}...{% endblock %}`

```html
{% extends "base.html" %}
{% block content %}
    <div class="row">
      <div class="col-8">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
          <div class="alert alert-warning" role="alert">
            {% for message in messages %}
                {{ message }}<br>
            {% endfor %}
          </div>
          {% endif %}
        {% endwith %}
        <h2>Новости</h2>
        {% for news in news_list %}
        <h3><a href="{{news.url}}">{{news.title}}</a></h3>
        <p>{{news.published}}</p>
        <hr/>
        {% endfor %}        
      </div>
      <div class="col-4">
        <h2> Прогноз погоды</h2>
        {% if weather %}
          {{ weather.temp_C }}, ощущается как {{ weather.FeelsLikeC }}
        {% else %}
          Сервис погоды недоступен
        {% endif %}
      </div>
    </div>
{% endblock %}
```

- В начале файла добавим строку `{% extends "base.html" %}`

- А в `news.views.index` поменяем название шаблона в функции `render_template` с `index.html` на `news/index.html`

```python
"""
webapp2/news/views.py
"""
...
return render_template(
        "news/index.html", title=page_title, weather=weather, news_list=news_list
    )
```

### 6 - Главное меню

Используем стандартный компонент <b>Navbar</b> из библиотеки Bootstrap.
Самый простой вариант - скопировать html-код. компонент и вставить base.html

1. Создаем файл `templates/menu.html`, скопируем туда код компонента и в base.html добавте строку.
`{% include 'menu.html' %}`

Копия навбара
```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">Новости</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/">Главная страница</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="{{url_for('user.login')}}">Логин</a>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Искать</button>
    </form>
  </div>
</nav>
```
### 7 - Создание декаратора @admin_required

`Декоратор` - Функция-обертка которая позволяет выполнять какие-то действия перед вызовом декорируеой функции не изменяя её.

Например декоратор `@login_required` проверяет, что пользователь авторизован и если нет - перенаправляет на страницу логина не вызывая декорируемую функцию. А если пользователь авторизован, то декорируемая функция вызывается "Прозрачно", как будто декоратора нет.


- Сделаем собственный декоратор @admin_required

Сначала посмотрим как устроен декаратор `@login_required`

Мы видим, что внутри конструкция if/elif которая проверяет, авторизован ли пользователь. Если да, то функция вызывает декорируемую функцию `return func(*args, **kwargs)`. Чтобы сделать

- Сделаем собственный декоратор
Создадим файл `user/decorators.py` и доавим туда импорты.

Декораторы хранятся в соответствующейм Blueprint

```python
from functools import wraps

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user
```

- Сделаем собственный декоратор

```python
def admin-required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin():
            flash('Эта страница тебе не доступна.')
            return redirect(url_for('news.index'))
        return func(*args, **kwargs)
    return decorated_view
```

-------------------------------------

## Week 8 
-------------------------------
1. Скрипт для запуска приложений
2. Что такое миграции
3. Создаем первую миграцию
4. Добавим поле в модель
5. Регистрация пользователей
6. Работа пользователей в шаблоне
7. Дополнительные проверки в форме
-----------------------------------

### 1. Скрипт для запуска приложений.
-------------

Скрипты для запуска

`.bat` - Для Windows
`.sh` - Для линукс и MacOs

----------------

#### Скрипт для Windows
В Корне проекта создается `run.bat` с добавлением
`set FLASK_APP=webapp2 && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run`

Для запуска проекта можно просто написать в консоли `run.bat`

-------------------

#### Скрипт для Linux/MacOs

- В корне созд. файл `run.sh`:

```bash
#!/bin/sh
export FLASK_APP=webapp2 && export FLASK_ENV=development && flask run
```
- После сохранения кода выполнить
`chmod +x run.sh` - Это сделает файл исполняемым.
`./run.sh` - Запуск скрипта. 
`/` - из этой директории
----------------

### 2. Что такое миграции
------------

При внесении изменений в модели - эти изменения не появятся в базе данных сами собой.

`Миграции` - python скрипты, которые вносят изменения в нашу бд автоматически.

<h1>Flask-Migrate</h1>  позволяет отслеживать изменения в моделях, и генерировать скрипты миграции автоматически. Пакет построен на базе Alembic - системы миграции для SQLAlchemy.

- Добавление в модель новового поля user.models.User

```python
...

class User(db.Model, UserMixin):
    ...

    email = db.Column(db.String(50), unique=True)
```

--------------------

### 3. Создаем первую миграцию

<h1>Включим поддержку миграций</h1>

1. Добавить в `__init__.py`

```python
from flask-migrate import Migrate
...

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
```

Внесем изменения в файл конфигураации.
`config.py`

`SQLALCHEMY_TRACK_MODIFICATIONS = False`

<h1>Инициализируем механизм миграций.</h1>

Для работы Flask-Migrate нужно создать нескольколь файлов и папок. Процесс автоматизирован, нам нужно выполнить команду:

Linux и Mac: `export FLASK_APP=webapp2 && flask db init`
Windows: `set FLASK_APP=webapp2 && flask db init`

<h1>Создадим первую миграцию</h1>

У нас создана база данных, поэтому чтобы посмотреть как работают миграции, переиминуем нашу бд
`webapp2.db`

Linux и Mac: `mv webapp.db webapp.db.old`

Windows: `move webapp.db webapp.db.old`

<h1>Создадим первую миграцию.</h1>

Linux и Mac: `export FLASK_APP=webapp2 && flask db migrate -m "users and news tables"`

Windows: `set FLASK_APP=webapp2 && flask db migrate -m "users and news tables"`

В `migrations/versions/`  появился первый файл вида `hex_users_and_news_table.py` внутри в секции `upgrade()` написан код для создания таблиц.

В секции `downgrade()` прописано удаления таблиц.

<h1>Примение миграции.</h1>

Миграция применяется командой `flask db upgrade` и если мы выполним её, то появится новый файл webapp.db. Там будет правиоьная структура, но не будет даннх. 
Теперь файл `create_db.py` не нужен, можно удалить.

Сделаем очередной мув.

`mv webapp.db.old webapp.db`

<h1>Миграции и существующие таблицы.</h1>
У нас есть база со структурой и данными. Если мы попробуем выполнить миграцию на ней, то получим mv/move. 
Усли мы попробуем выполнить миграцию, то получим ошибку.
Чтобы работать с миграциями на существующей базе, нам нужно пометить нашу миграцию как выполненную командой `flask db stamp hex`.

Если мы теперь увидим что там появилась новая таблица `alembic_version`

------------------------

### 4. Добавим поле в модель User

Для того, чтобы добавить на сайт регистрацию, нам понадобится поле `email` в модели `User`:

```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, promary_key=True)
    username = db.Column(dn.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))
```

Создадим миграцию и выполним ее.

`flask db migrate -m "added email to user"`

`flask db upgrade`

Зайдем в базу данных и проверим, что в таблице `user` появилось новое поле.

------------------

### 5. Регистрация пользователей

Форма регистрации похожа на форму логина, но мы добавим пару доп. полей.

```python
class RegistrationForm(FlaskForm):
    username = StringField('Имя Пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired()],
        render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
        render_kw={"class": "form-control"})
    password2 = PasswordField('Повтори пароль', validators=[DataRequired()],
        render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
```

<h1>Добавим пару стандартных валидаторов</h1>

Ранее был использован валидатор `DataRequired`, который проверя, что поле не пустое. Добавим валидаторы `Email` и `EqualTo` - они проверяют, что значение одного поля идентично значению другого.

```python
from wtforms.validators import DataRequired, Email, EqualTo
...

email = StringField('Email', validators=[DataRequired(), Email()],
    render_kw={"class": "form-control"})
password = PasswordField('Пароль', validators=[DataRequired()], 
    render_kw={"class": "form-control"})
password2 = PasswordField('Пароль', validators=[DataRequired(), EqualTo('password')],render_kw={"class": "form-control"})

```

<h1>Добавим шаблон</h1>

Скопируем файл `templates/user/login.html` как `templates/user/registration.html` и поменяем форму под наши поля.

```html
{% extends "base.html" %}
{% block content %}
    <div class="row">
      <div class="col-4">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
          <div class="alert alert-warning" role="alert">
            {% for message in messages %}
              {{ message }}<br>
            {% endfor %}
          </div>
          {% endif %}
        {% endwith %}
        <form action="{{url_for('user.process_login')}}" method="post">
          {{ form.hidden_tag() }}
          <div class="form-group">
            {{ form.username.label }}
            {{ form.username() }}
          </div>
          <div class="form-group">
            {{ form.email.label }}
            {{ form.email() }}
          </div>
          <div class="form-group">
            {{ form.password.label }}
            {{ form.password() }}
          </div>
          <div class="form-group">
            {{ form.password2.label }}
            {{ form.password2() }}
          </div>
          {{ form.submit() }}         
        </form>
           
      </div>
      <div class="col-8">

      </div>
    </div>
{% endblock %}

```


<h1>Cтраница регистрации</h1>

<p>Сделана форма и шаблон, но чтобы все заработало, нужно добавить соответствующие route-ы и функции обработчики. Первая функция будет просто показыавть форму регистрации.</p>

Открываем User/views.py

```python
from webapp2.db import db
from webapp2.user.forms import LoginForm, RegistrationForm
```

- Функция регистрации

```python
@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('user/registration.html', page_title=title, form=form)
```

<h1>Обработчик регистрации</h1>

```python
@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегестрировались!')
        return redirect(url_for('user.login'))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.register'))
```

----------------

### 6. Работа с пользовательскими шаблонами.
<h1>Работа с  пользователем в шаблоне.</h1>

<p>Flask-Login дает нам возможность обращатся к `current_user` в шаблоне:</p>
menu -> login->

```html
{% if current_user.is_authenticated %}
    <a class="nav-link" href="{{ url_for('user.logout') }}"> Выйти </a>
{% else %}
    <a class="nav-link" href="{{url_for('user.login')}}"> Войти </a>
{% endif %}
```

- Поправим код согласно канону

```html
...

 <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/">Главная страница</a>
      </li>

    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Искать</button>
    </form>
    <ul class="navbar-nav">
        <li class="nav-item">
        {% if current_user.is_authenticated %}
        <a class="nav-link" href="{{ url_for('user.logout') }}"> Выйти </a>
        {% else %}
        <a class="nav-link" href="{{url_for('user.login')}}"> Войти </a>
        {% endif %}
        
      </li>
      
    </ul>
  </div>
```
upgrade:

```html
<ul class="navbar-nav">
        {% if current_user.is_authenticated %}
        <li class="nav-item">
            <span class="nav-link">Привет, {{ current_user.username }}</span>
        </li>
        {% if current_user.is_admin %}
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('admin.admin_index') }}"> Админка </a>
        </li>
        {% endif %}
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('user.logout') }}"> Выйти </a>
        </li>
        {% else %}
        <li class="nab-item">
            <a class="nav-link" href="{{ url_for('user.register') }}"> Регистрация </a>
        </li>
        <li class="nab-item">
            <a class="nav-link" href="{{url_for('user.login')}}"> Войти </a>
        </li>
        {% endif %}
      
    </ul>
```

### 7. Дополнительные проверки в форме.
<h1>Дополнительные проверки</h1>

<p>Если пользователь при регистрации укажет имя которое уже есть в системе, то мы получим ошибку данных. Добавим собственные валидаторы для полей формы. Валидатор-это просто метод класса формы, имя которого строится как `validate_ПОЛЕ`, например `validate_email`. В случае ошибки валидатор должен выкидывать исключение `wtforms.validators.ValidationError`</p>

```python
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp2.user.models import User
```

- Файл дополняется в `webapp2/user/forms.py`

```python
class RegistrationForm(FlaskForm):
    ...

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationErroe('Пользователь с таким именем уже зарегестрирован')

    def validate_email(self,email):
        users_counts = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегестрирован')

```

<h1>Вывод ошибок в шаблоне.</h1>

- Будем передавать ошибки в форме при помощи `flash`

```python
def process_reg():
    ...
else:
    for field, errors in form.errors.items():
        for errors in errors:
            flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, errors
            ))
    return redirect(url_for('user.register'))
```

- Далее в `webapp2/user/register.html`

```html
  {% with message = get_flashed_messages() %}
    {% if messages %}
      {% for message in messages %}
      <div class="alert alert-danger" role="alert">
          {{ message }}
      </div>
      {% endfor %}
    {% endif %}
  {% endwith %}
```


## Week 9
1. Создадим отдельный модуль для получения новостей
2. Соберем сниппеты с Хабрхабр
3. Обработаем тексты новостей
4. Рассмотрим страницы статей на сайте
5. Знакомство с Celery
6. Узнаем о выполнении задач по расписанию.

### 1. Создадим отдельный модуль для получения новостей
<p>Реализация сбора новостей с хабра.</p>

#### Разобьем процесс на несколько шагов.
1. Получение страницы со списком новостей.
2. Сбор с неё ссылок на новости.
3. Проверка, каих новостей у нас еще нет.
4. СБор полного текста для каждой новости.


#### Сделаем отдельный модуль для сбора новостей.
Мы услужняем сбор новостей и возможно будем собирать новости из разных из
разных источников. Создадим папку `webapp2/news/parsers/` и вней `__init__.py`,
`utils.py`, `habr.py`.


---------------

<h1>User-Agent</h1>
<p>Браузер делает запрос к сайту, он "представляется" отправляяя заголовок User-Agent. Либа requests по-умолчанию "представляется" как python-requests и некоторые сайты могут ограничить доступ к своему контенту по этому признаку.</p>

<p>Библиотека requests дает нам возможность посылать свои header-ы.
Скопируем значение User-Agent из браузера, и будем подставять при запросе.</p>


<h1>Добавим User-Agent в get_html</h1>

headers - Просто словарь.

```python
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    try:
        result = requests.get(url, headers=headers)
        ...
```

#### Сбор сниппетов новостей
<p>Собираем `title`, `url`, `Дату новостей`,  и кладываем их в БД.</p>

`habr.py`


```python
from bs4 import BeautifulSoup
from datetime import datetime


from webapp2.news.parsers.utils import get_html, save_news
```

<h1><Перепишем <b>get_habr_snippets</b></h1>

`Сниппеты` - Небольшой новостной блок


```python
from bs4 import BeautifulSoup

from webapp2.news.parsers.utils import get_html, save_news

def get_habr_snippets() -> str:
    html = get_html(
        "https://habr.com/ru/search/?q=Python&target_type=posts&order=date"
    )
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find("div", class_="tm-articles-list").findAll("div", class_="tm-article-snippet")        
        for news in all_news:
            title = news.find("a", class_="tm-article-snippet__title-link").text
            url = news.find("a", class_="tm-article-snippet__title-link")["href"]
            published = news.find("span", class_="tm-article-snippet__datetime-published").text
            print(title, url, published)


```

### 2. Соберем сниппеты с Хабрхабр

<b>Выставим русскоязычную локаль для распознования даты.</b>

`habr.py`
Выставление локали отличается на Mac/Linux и Windows

```python
from datetime import datetime, timedelta
import locale
import platform

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LG_TIME, 'ru_RU')

```

<b>Напишем функцию Перевода даты</b>

```python
def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()
```

<b>Измененный скрипт `habr.py` </b>

```python
from datetime import datetime, timedelta
import locale
import platform
from bs4 import BeautifulSoup

from webapp2.news.parsers.utils import get_html, save_news

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


def parse_habr_date(date_str):
    if "сегодня" in date_str:
        today = datetime.now()
        date_str = date_str.replace("сегодня", today.strftime("%d %B %Y"))
    elif "вчера" in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace("вчера", yesterday.strftime("%d %B %Y"))
    try:
        return datetime.strptime(date_str, "%d %B %Y в %H:%M")
    except ValueError:
        return datetime.now()


def get_habr_snippets() -> str:
    html = get_html("https://habr.com/ru/search/?q=Python&target_type=posts&order=date")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find("div", class_="tm-articles-list").findAll(
            "div", class_="tm-article-snippet"
        )
        for news in all_news:
            title = news.find("a", class_="tm-article-snippet__title-link").text
            url = news.find("a", class_="tm-article-snippet__title-link")["href"]
            published = news.find(
                "span", class_="tm-article-snippet__datetime-published"
            ).text
            published = parse_habr_date(published)
            save_news(title, 'https://habr.com'+ url, published)

```

### 3. Обработаем тексты новостей
<p>Получение текстов новостей</p>

Последовательность действий.
1. Возьмем из базы все новости, у которых пустой `text`
2. Для каждой новости сделаем запрос на `url`
3. Получим html и выберем из него текст новости
4. Сохраним текст в новости в базу.


<b>Получим список новостей, у которых нет текста</b>
Простой запрос к базе данных, если мы не добавляли текст, значит в поле будет `NULL` и мы сможем обратиться к таким полям через is_(None)

```python
def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
```

<b>Получим текст статьи и сохраним его</b>
Мы будем испольщовать `decode_contents`

```python
if html:
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='post__text-html').decode_contents()
    if article:
        news.text = article
        db.session.add(news)
        db.session.commit()
```

### 4. Рассмотрим страницы статей на сайте

Добавим view для статей и проставим наних ссылки с главной

```python
from flask import abort, Blueprint, current_app, render_template

@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news:
        abort(404)

    return render_template('news/single_news.html', page_title=my_news.title, news=my_news)
```

<b>Поправим стили</b>

```css
.news-content img {
    max-wodth: 100%
}
```


И подключим его в `base.html`
`<link rel="stylesheet" href={{url_for('static', filename='style.css')}}`

<b>Добавим форматирование кода.</b>
```html
<link rel="stylesheet"
href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.13.1/styles/default.min.css">
<script
src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.13.1/highlight.min.js">
</script>
<script>hljs.initHighlightingOnLoad();</script>
```

<b>Ссылки на страницы</b>
Замена ссылок новостей.
Змена в `index.html`

`href="{{ url_for('news.single_news', news_id=news.id) }}"`

Измененный `news/views.py`

```python
"""
Работа с блюпринтами
"""
from flask import abort, Blueprint, current_app, render_template

from webapp2.news.models import News
from weather2 import weather_by_city


# Основной роутинг. Префикса не будет
blueprint = Blueprint("news", __name__)


@blueprint.route("/")
def index() -> str:
    page_title = "Новости Python"
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    return render_template(
        "news/index.html", title=page_title, weather=weather, news_list=news_list
    )

@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news:
        abort(404)

    return render_template('news/single_news.html', page_title=my_news.title, news=my_news)
```

### 5. Знакомство с Celery
Сейчас сбор проиходит в ручную. Нам необходимо автоматизировать сбор. 
Celery наш выбор

Он используется в проекта, когда нужно выполнять задачи асинхронно (не занимая время веб-сервера) или запускать их по расписанию.

<b>Установка зависимостей</b>
Для работы понадобится установить Redis. Redis бд типа ключ-значение, которую Celery будет использовать для хранения очереди задач.

Инсталл
`apt-get install redis-server`

<b>Установка Celery</b>
`pip install calery[redis]`

<b>Создадим тестовый таск</b>
Такс - функция, обернутая в декоратор `celery.task`. Такую функцию можно вызвать напрямую, так и передавать на исполнение Celery при помощи метода `delay()`


<b>Создадим тестовй таск</b>
Создадим `tasks.py` в корне проекта и сделаем таск, который складывает два числа:

```python
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def add(x, y):
    print(x + y)
```

<b>Запустим Celery</b>

<b>Linux/Mac - </b> `celery -A tasks worker --loglevel=info`

<b>Windows - </b> `set FORKED_BY_MULTIPROCESSING=1 && celery -A tasks worker --loglevel=info`


Чтобы начало работать надо добвить
```python
from tasks import add

add.delay(234,234)
```

`add.delay` производит асинхронный вызов.


### 6. Выполнение задач по расписанию.

```python
from webapp2 import create_app
from webapp2.news.parsers import habr

flask_app = create_app()

@celery_app.task
def habr_snippets():
    with flask_app.app_context():
        habr.get_news_snippets()


@celery_app.task
def habr_content():
    with flask_app.app_context():
        habr.get_news_content()


```

Открываем второе окно терминала и переходим по дерикториям до проекта
в нем включаем python
```python
>>> from tasks import habr_snippets

>>> habr_snippets.delay()
```

<b>Автозапуск по времени</b>

Используем модуль `cron` из celery и добавим при запуске celery расписание.

```python
from celery.schedules import crontab

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), habr_snippets.s())
```

<b>Запустим Celery-beat</b>
<p>Celery-beat - запускает работу задач по расписанию. Он следит за расписанием и отправляет задачи worker-am. Beat нужно запускать отдельно, пожтому понадобится еще одно окно терминала.</p>

`celery -A tasks beat`


Если проект простой, можно использовать такое:
`celery -A tasks worker -B --loglevel=INFO`