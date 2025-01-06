from .. import app
from flask import render_template

@app.get("/")
def index():
    return render_template("base.html")