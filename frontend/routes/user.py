from requests import get
from flask import render_template
from .. import flask_app, BACKEND_URL


@flask_app.get("/users/<int:id>")
def get_user(id):
    user = get(f"{BACKEND_URL}/users/{id}")
    if user:
        return render_template("user_profile.html", user=user.json())
