from requests import get, put
from flask import render_template, flash, redirect, url_for, request
from .. import flask_app, BACKEND_URL
from ..forms import EditUserForm


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


@flask_app.get("/users/edit/<int:id>")
def edit_user_page(id):
    user_response = get(f"{BACKEND_URL}/users/{id}")
    form = EditUserForm()
    if user_response.status_code == 200:
        return render_template("edit_user.html", user=user_response.json(), form=form)
    else:
        flash(f"User with id {id} not found.", "danger")
        return redirect(url_for("index"))


@flask_app.post("/users/edit/<int:id>")
def edit_user(id):
    form = EditUserForm()
    if form.validate_on_submit():
        name = form.name.data
        bio = form.bio.data

        token = request.cookies.get("token")

        if not token:
            flash("You need to log in to update your profile!", "danger")
            return redirect(url_for("login"))

        headers = {"Authorization": f"Bearer {token}"}

        response = put(
            f"{BACKEND_URL}/users/{id}",
            headers=headers,
            params={"name": name, "bio": bio},
        )

        if response.status_code == 200:
            flash("Profile updated successfully!", "success")
            return redirect(url_for("get_user", id=id))
        else:
            flash(
                f"Failed to update profile: {response.json().get('detail', 'Unknown error')}",
                "danger",
            )
            return redirect(url_for("edit_user_page", id=id))
    else:
        flash("Invalid form data.", "danger")
        return redirect(url_for("edit_user_page", id=id))
