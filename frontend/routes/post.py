from requests import get
from flask import render_template, redirect, flash, url_for, request
from .. import flask_app, BACKEND_URL


@flask_app.get("/users/<int:id>/create_post")
def create_post_page(id):

    user_response = get(f"{BACKEND_URL}/users/{id}")

    if user_response.status_code == 200:
        user = user_response.json()
    else:
        user = None

    return render_template("create_post.html", user=user)


@flask_app.post("/users/<int:id>/create_post")
def create_post(id):
    title = request.form.get("title")
    content = request.form.get("content")
    image = request.files.get("image")

    if not title or not content:
        flash("Title and content are required.")
        return redirect(url_for("create_post_page", id=id))

    response = get(
        f"{BACKEND_URL}/posts",
        params={"title": title, "content": content, "user_id": id, "image": image},
    )

    if response.status_code == 201:
        flash("Post created successfully!")
    else:
        flash("There was an issue creating the post.")

    return redirect(url_for("get_user", id=id))
