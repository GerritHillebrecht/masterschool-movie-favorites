from flask import Blueprint, redirect, url_for, render_template, flash, current_app
from flask_login import current_user, login_user, logout_user
from forms import LoginForm, RegistrationForm
from schemas import User

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('static_routes.get_index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data
        )
        user.set_password(form.password.data)
        current_app.data_manager.add_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for("auth.get_login"))

    return render_template('register.html', title='Register', form=form)


@auth_routes.route("/login", methods=["GET", "POST"])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('static_routes.get_index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.get_login'))
        login_user(user)
        return redirect(url_for('static_routes.get_index'))

    return render_template('login.html', title='Sign In', form=form)


@auth_routes.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('static_routes.get_landing_page'))
