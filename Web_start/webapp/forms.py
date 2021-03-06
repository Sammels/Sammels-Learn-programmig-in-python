from flask_wtf import FlaskForm

# Импортируем типы полей
from wtforms import BooleanField, StringField, PasswordField, SubmitField

# Импортируем валидатор. Который проверяет, что пользователь действительно
# ввел данные
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # 1 параметром передаем label подпись к полю формы
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        "Отправить",
        render_kw={"class": "btn btn-primary"}
    )
    remember_me = BooleanField(
        "Запомнить меня",
        default=True,
        render_kw={"class": "form-check-input"}
    )
