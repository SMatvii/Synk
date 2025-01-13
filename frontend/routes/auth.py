import requests
from dotenv import load_dotenv
from .. import app
from flask import Blueprint, render_template, redirect, url_for, request
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
    pass


@app.get("/login")
def login():
    form = LoginForm()
    form.title = "Login"
    return render_template("auth.html", form=form)


@app.post("/login")
def login_post():
    form = LoginForm()
    pass
