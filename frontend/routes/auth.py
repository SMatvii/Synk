from os import getenv
from requests import post
from dotenv import load_dotenv
from flask import render_template, redirect, url_for, request
from .. import flask_app, BACKEND_URL
from ..forms import RegisterForm, LoginForm



load_dotenv()



@flask_app.get("/register")
def register():
    form = RegisterForm()
    form.title="Register"
    return render_template("auth.html", form=form)


@flask_app.post("/register")
def register_post():
    form = RegisterForm()
    data = {
        "name": form.name.data,
        "email": form.email.data,
        "password": form.password.data,
        "bio": "",
    }
    resp = post(f"{BACKEND_URL}/users/registrate", json=data)
    if resp.status_code == 201:
        return redirect(url_for("login"))


@flask_app.get("/login")
def login():
    form = LoginForm()
    form.title = "Login"
    return render_template("auth.html", form=form)


@flask_app.post("/login")
def login_post():
    form = LoginForm()
    data = {"username": form.name.data, "password": form.password.data}
    resp = post(f"{BACKEND_URL}/auth/token", data=data)
    if resp.ok:
        response = redirect(url_for("index"))
        response.set_cookie("token", resp.json().get("access_token"))
        return response 
    

@flask_app.get("/token")
def get_token():
    token = request.cookies.get("token")
    return "<h1>Your access token: " + token + "</h1>"
