from flask import render_template
from .. import app


@app.get("/")
def index():
    return render_template("base.html")
