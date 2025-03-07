from requests import get, post, put, delete
from flask import render_template, redirect, flash, url_for, request
from .. import flask_app, BACKEND_URL
from ..forms import PostForm, EditPostForm, CommentForm


@flask_app.get("/posts/create")
def create_post_page():
    form = PostForm()
    return render_template("post.html", form=form, method="POST", action="Create")


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

        response = post(
            f"{BACKEND_URL}/posts",
            headers=headers,
            params={
                "title": title,
                "content": content,
            },
            files=files,
        )

        if response.status_code == 201:
            flash("Post created successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash(f"There was an issue creating the post. {response.json()}", "danger")
            return redirect(url_for("create_post_page"))

    else:
        flash("Form validation failed. Please try again.", "danger")
        return redirect(url_for("create_post_page"))


@flask_app.get("/posts/<int:id>")
def see_one_post(id):
    post = get(f"{BACKEND_URL}/posts/{id}")
    if post:
        form = CommentForm()
        user_id = post.json().get("user_id")
        user = get(f"{BACKEND_URL}/users/{user_id}")
        comments = get(f"{BACKEND_URL}/comments/post/{id}")
        if comments.status_code == 200:
            return render_template(
                "one_post.html",
                post=post.json(),
                user=user.json(),
                url=BACKEND_URL,
                comments=comments.json(),
                form=form,
            )
        else:
            return render_template(
                "one_post.html",
                post=post.json(),
                url=BACKEND_URL,
                user=user.json(),
                form=form,
            )
    else:
        flash(f"No post with this id: {id}. Create some first.", "danger")
        return redirect(url_for("create_post_page"))


@flask_app.post("/posts/<int:id>")
def see_post(id):
    form = CommentForm()
    content = form.content.data
    token = request.cookies.get("token")

    if not token:
        flash("You need to log in to create a comment!", "danger")
        return redirect(url_for("login"))

    data = {"content": content, "post_id": id}

    headers = {"Authorization": f"Bearer {token}"}
    resp = post(f"{BACKEND_URL}/comments", json=data, headers=headers)
    if resp.status_code == 201:
        flash("Comment created!")
        return redirect(url_for("see_one_post", id=id))
    else:
        flash(f"Error:{resp.json()}")
        return redirect(url_for("see_one_post", id=id))


@flask_app.get("/posts/edit/<int:id>")
def edit_post_page(id):
    resp = get(f"{BACKEND_URL}/posts/{id}")
    if resp.status_code == 200:
        form = EditPostForm()
        return render_template("post.html", form=form, method="POST", action="Edit")
    else:
        flash(resp.json())
        return redirect(url_for("index"))


@flask_app.post("/posts/edit/<int:id>")
def edit_post(id):
    form = EditPostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        token = request.cookies.get("token")

        if not token:
            flash("You need to log in to create a post!", "danger")
            return redirect(url_for("login"))

        headers = {"Authorization": f"Bearer {token}"}

        response = put(
            f"{BACKEND_URL}/posts/{id}",
            headers=headers,
            json={
                "title": title,
                "content": content,
            },
        )

        if response.status_code == 200:
            flash("Post edited successfully!", "success")
            return redirect(url_for("see_one_post", id=id))
        else:
            flash(f"There was an issue editing the post. {response.json()}", "danger")
            return redirect(url_for("edit_post_page", id=id))
    else:
        flash("Form validation failed. Please try again.", "danger")
        return redirect(url_for("edit_post_page", id=id))


@flask_app.post("/posts/delete/<int:id>")
def delete_post(id):

    token = request.cookies.get("token")

    if not token:
        flash("You need to log in to delete a post!", "danger")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}

    response = delete(
        f"{BACKEND_URL}/posts/{id}",
        headers=headers,
    )

    if response.status_code == 204:
        flash("Post deleted successfully!", "success")
    else:
        flash(f"Error deleting post: {response.json()}", "danger")
    return redirect(url_for("index"))


@flask_app.get("/posts/users/delete/<int:id>")
def delete_user_posts(id):
    token = request.cookies.get("token")
    if not token:
        flash("You need to log in to delete posts!", "danger")
        return redirect(url_for("login"))
    
    headers = {"Authorization": f"Bearer {token}"}

    resp = delete(f"{BACKEND_URL}/posts/users/{id}", headers=headers)
    if resp.status_code == 200:
        flash("Successfuly deleted")
        return redirect(url_for("index"))
    else:
        flash(f"Error:{resp.json()}")
        return redirect(url_for("index"))
