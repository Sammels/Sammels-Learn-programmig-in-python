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

