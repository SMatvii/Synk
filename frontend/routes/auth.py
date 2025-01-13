from os import getenv
from requests import post
from dotenv import load_dotenv
from flask import render_template, redirect, url_for, request
from .. import app
from ..forms import RegisterForm, LoginForm


load_dotenv()
BACKEND_URL = getenv("BACKEND_URL")


@app.get("/register")
def register():
    form = RegisterForm()
    return render_template("auth.html", form=form)


@app.post("/register")
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


@app.get("/login")
def login():
    form = LoginForm()
    form.title = "Login"
    return render_template("auth.html", form=form)


@app.post("/login")
def login_post():
    form = LoginForm()
    data = {"username": form.name.data, "password": form.password.data}
    resp = post(f"{BACKEND_URL}/auth/token", data=data)
    if resp.ok:
        return redirect(url_for("index"))
