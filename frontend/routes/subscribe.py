from requests import get, post, put, delete
from flask import render_template, redirect, flash, url_for, request
from .. import flask_app, BACKEND_URL


@flask_app.get("/subscribe/<int:id>")
def subscribe(id):
    token = request.cookies.get("token")

    if not token:
        flash("You need to log in to subscribe!", "danger")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}

    resp = post(f"{BACKEND_URL}/sub/{id}", headers=headers)

    if resp.status_code == 200:
        flash("Subscribed successfully!")
        return redirect(url_for("get_user", id=id))
    else:
        flash(f"Error: {resp.json()}!")
        return redirect(url_for("get_user", id=id))


@flask_app.get("/unsubscribe/<int:id>")
def unsubscribe(id):
    token = request.cookies.get("token")

    if not token:
        flash("You need to log in to subscribe!", "danger")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}

    resp = post(f"{BACKEND_URL}/sub/un/{id}", headers=headers)

    if resp.status_code == 200:
        flash("Unsubscribed successfuly!")
        return redirect(url_for("get_user", id=id))
    else:
        flash(f"Error: {resp.json()}!")
        return redirect(url_for("get_user", id=id))


@flask_app.get("/users/<int:id>/subscribers")
def get_subscribers(id):
    resp = get(f"{BACKEND_URL}/sub/subscribers/{id}")

    if resp.status_code == 200:
        return render_template(
            "sub.html", title="Subscribers", users=resp.json().get("subscribers")
        )
    else:
        flash(f"Error:{resp.json()}")
        return redirect(url_for("get_user"), id=id)


@flask_app.get("/users/<int:id>/subscriptions")
def get_subscriptions(id):
    resp = get(f"{BACKEND_URL}/sub/subscriptions/{id}")

    if resp.status_code == 200:
        return render_template(
            "sub.html", title="Subscriptions", users=resp.json().get("subscriptions")
        )
    else:
        flash(f"Error: {resp.json()}!")
        return redirect(url_for("get_user", id=id))
