from flask import redirect, url_for, render_template, flash, request
from flask_login import (current_user, login_user, logout_user, login_required)

from campus_gist import app, db
from campus_gist.forms import (RegistrationForm, LoginForm, CreateGistForm,
                               UpdateGistForm)
from campus_gist.models import Student


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/gists")
def show_all_gists():
    return render_template("gists.html")

# gists/gist_id
@app.route("/gist")
def current_gist():
    return render_template("current_gist.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    # Redirect authenticated user
    if current_user.is_authenticated:
        return redirect(url_for("show_all_gists"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=form.username.data).first()
        # Check if username and password is invalid and redirect to login page
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f"Welcome back {user.fullname}!")

            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("show_all_gists"))
        else:
            flash("Invalid username or password!!")
            return redirect(url_for("login_page"))
    return render_template("auth/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bye Bye!! See you next time.")
    return redirect(url_for("show_all_gists"))


@app.route("/register", methods=["GET", "POST"])
def register_page():
    # Redirect authenticated user
    if current_user.is_authenticated:
        return redirect(url_for("show_all_gists"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Convert the institutions to Dictionary the choose the institution
        # the user selected from the dict.
        institute = dict(form.instututions.choices).get(form.instututions.data)
        user = Student(fullname=form.fullname.data, email=form.email.data,
                       username=form.username.data,
                       institutions=institute)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Successfully Registered an Account!")
        return redirect(url_for("show_all_gists"))
    return render_template("auth/register.html", form=form)


@app.route("/account")
@login_required
def account_page():
    return render_template("auth/profile.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update_gist_page():
    form = UpdateGistForm()
    return render_template("auth/update_gist.html", form=form)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_gist_page():
    form = CreateGistForm()
    return render_template("auth/create_gist.html", form=form)


@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile_page(username):
    user = Student.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template("auth/profile.html", user=user, posts=posts)
