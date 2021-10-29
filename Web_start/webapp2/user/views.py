from webapp2.user.forms import LoginForm, RegistrationForm
from webapp2.user.models import User
from webapp2.db import db

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

# blueprint = Blueprint("Название бп", имя модуля можно и так оставлять,
# url_prefix - то с чего будут начинатся все юрлы)
blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login")
def login():
    # Если пользватель авторизован редирект на главную
    if current_user.is_authenticated:
        return redirect(url_for("news.index"))
    title = "Авторизация"
    # Нужно создать экземпляр формы (класс), некое формальное описание
    # чтобы работать с формой
    login_form = LoginForm()
    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы вошли на сайт")
            return redirect(url_for("user.login"))

    flash("Неправильное имя пользователя или пароль")
    return redirect(url_for("user.login"))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('user/registration.html', page_title=title, form=form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегестрировались")
        return redirect(url_for('user.login'))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.register'))


@blueprint.route("/logout")
def logout():
    # Реализация окончание сессии
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("news.index"))
