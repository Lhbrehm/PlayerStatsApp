from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')

                user = User.query.filter_by(email=email).first()
                if user:
                        if check_password_hash(user.password, password):
                                flash("Logged in", category="success")
                                login_user(user, remember=True)
                                return redirect(url_for('views.home'))
                        else:
                                flash('Incorrect Password', category="error")
                else:
                        flash('User does not exist', category="error")

        return render_template('login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
        logout_user()
        return redirect(url_for("auth.logout"))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
        if request.method == 'POST':
                email = request.form.get('email')
                first_name = request.form.get('firstName')
                password1 = request.form.get('pw1')
                password2 = request.form.get('pw2')

                user = User.query.filter_by(email=email).first()
                if user:
                        flash('Email already exists', category="error")
                        pass
                elif len(email) < 4:
                        flash('Email must be greater than 4 characters', category="error")
                        pass
                elif len(first_name) < 2:
                        flash('First name must be greater than 2 characters', category="error")
                        pass
                elif password1 != password2:
                        flash('Passwords must match', category="error")
                        pass
                elif len(password1) < 7:
                        flash('Password must be 8+ characters', category="error")
                        pass
                else:
                        new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))
                        db.session.add(new_user)
                        db.session.commit()
                        login_user(new_user, remember=True)
                        flash('Account created', category="success")
                        return redirect(url_for("views.home"))

        return render_template('signup.html', user = current_user)
