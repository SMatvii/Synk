from requests import get
from dotenv import load_dotenv
from .. import app, BACKEND_URL
from flask import render_template, redirect, url_for, request
from ..forms import RegisterForm, LoginForm
from os import getenv

@app.get("/users/<int:id>")
def get_user(id):
    user = get(f"{BACKEND_URL}/users/{id}")
    if user:
        return render_template("user_profile.html", user=user.json())