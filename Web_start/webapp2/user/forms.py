from flask_wtf import FlaskForm

# Импортируем типы полей
from wtforms import BooleanField, StringField, PasswordField, SubmitField

# Импортируем валидатор. Который проверяет, что пользователь действительно
# ввел данные
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp2.user.models import User


class LoginForm(FlaskForm):
    # 1 параметром передаем label подпись к полю формы
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
    remember_me = BooleanField(
        "Запомнить меня", default=True, render_kw={"class": "form-check-input"}
    )


# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя Пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        "Пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"},
    )

    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегестрирован')


    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегестрирован')
