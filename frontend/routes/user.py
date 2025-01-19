from requests import get
from flask import render_template, flash, redirect, url_for
from .. import flask_app, BACKEND_URL


@flask_app.get("/users/<int:id>")
def get_user(id):
    user = get(f"{BACKEND_URL}/users/{id}")
    if user.status_code == 200:
        posts = get(f"{BACKEND_URL}/posts/users/{id}")
        if posts.status_code == 200:
            return render_template(
                "user_profile.html", user=user.json(), posts=posts.json()
            )
        else:
            return render_template("user_profile.html", user=user.json())
    else:
        flash(f"No user with this id: {id}.", "danger")
        return redirect(url_for("index"))
