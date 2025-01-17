from flask import render_template
from .. import flask_app


@flask_app.get("/")
def index():
    return render_template("base.html")
