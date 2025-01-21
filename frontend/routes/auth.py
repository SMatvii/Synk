from requests import post
from dotenv import load_dotenv
from flask import render_template, redirect, url_for, request, flash
from .. import flask_app, BACKEND_URL
from ..forms import RegisterForm, LoginForm


load_dotenv()


@flask_app.get("/register")
def register():
    form = RegisterForm()
    form.title = "Register"
    return render_template("auth.html", form=form)


@flask_app.post("/register")
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "email": form.email.data,
            "password": form.password.data,
            "bio": form.bio.data,
        }
        resp = post(f"{BACKEND_URL}/users/registrate", json=data)
        if resp.status_code == 201:
            flash("Successfuly registered. Now login and you are ready to go")
            return redirect(url_for("login"))
        else:
            flash(f"{resp.json()}", "danger")
            return redirect(url_for("register"))

    else:
        flash("Form validation failed. Please try again.", "danger")
        return redirect(url_for("register"))


@flask_app.get("/login")
def login():
    form = LoginForm()
    form.title = "Login"
    return render_template("auth.html", form=form)


@flask_app.post("/login")
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        data = {"username": form.email.data, "password": form.password.data}
        resp = post(f"{BACKEND_URL}/auth/token", data=data)
        if resp.ok:
            response = redirect(url_for("index"))
            response.set_cookie("token", resp.json().get("access_token"))
            return response
        else:
            flash(f"{resp.json()}", "danger")
            return redirect(url_for("login"))
    else:
        flash("Form validation failed. Please try again.", "danger")
        return redirect(url_for("login"))


@flask_app.get("/token")
def get_token():
    token = request.cookies.get("token")
    flash(f"Your token: {token}")
    return redirect(url_for("index"))
