import requests
from flask import render_template
from .. import flask_app, BACKEND_URL


@flask_app.get("/")
def index():

    resp = requests.get(f"{BACKEND_URL}/posts")
    return render_template("card.html", posts=resp.json())
