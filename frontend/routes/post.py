import requests
from flask import render_template, redirect, flash, url_for, request
from .. import flask_app, BACKEND_URL
from ..forms import PostForm


@flask_app.get("/posts/create")
def create_post_page():
    form = PostForm()
    return render_template("post.html", form=form)


@flask_app.post("/posts/create")
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image = form.image.data

        token = request.cookies.get("token")

        if not token:
            flash("You need to log in to create a post!", "danger")
            return redirect(url_for("login"))

        headers = {"Authorization": f"Bearer {token}"}

        files = {}
        if image:
            files["image"] = image

        response = requests.post(
            f"{BACKEND_URL}/posts",
            headers=headers,
            params={"title": title, "content": content,},
            files=files,
        )

        if response.status_code == 201:
            flash("Post created successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("There was an issue creating the post.", "danger")
            return redirect(url_for("create_post_page"))

    else:
        flash("Form validation failed. Please try again.", "danger")
        return redirect(url_for("create_post_page"))


@flask_app.get("/posts/<int:id>")
def see_one_post(id):
    post = requests.get(f"{BACKEND_URL}/posts/{id}")
    if post:
        user_id = post.json().get("user_id")
        user = requests.get(f"{BACKEND_URL}/users/{user_id}")
        comments = requests.get(f"{BACKEND_URL}/comments/{id}")
        if comments.status_code == 200: 
            return render_template(
                "one_post.html", 
                post=post.json(), 
                user=user.json(),
                comments=comments.json()
                )
        else:
            return render_template(
                "one_post.html", 
                post=post.json(), 
                user=user.json(),
            )