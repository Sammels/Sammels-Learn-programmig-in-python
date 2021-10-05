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
    username = imput('Введите имя пользователя: ')

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
from flask_login import LoginMager
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