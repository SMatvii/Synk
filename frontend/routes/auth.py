from requests import post, get
from dotenv import load_dotenv
from .. import app
from flask import render_template, redirect, url_for, request
from ..forms import RegisterForm, LoginForm
from os import getenv



load_dotenv()
BACKEND_URL = getenv("BACKEND_URL")


@app.get("/register")
def register():
    form = RegisterForm()
    return render_template("auth.html", form=form)


@app.post("/register")
def register_post():
    form = RegisterForm()
    data = {"name": form.name.data,
            "email": form.email.data,
            "password": form.password.data,
            "bio": form.bio.data}
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
    data = {"username": form.name.data,
            "password": form.password.data}
    resp = post(f"{BACKEND_URL}/auth/token", data=data)
    if resp.ok:
        return redirect(url_for("index"))
    
app.get("/users/<int:id>")
def get_user(id):
    user = get(f"{BACKEND_URL}/users/{id}")
    if user:
        return render_template("user_profile.html", user=user)    
