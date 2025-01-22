from flask import render_template, redirect, flash, url_for, request
from requests import get, put, delete
from .. import flask_app, BACKEND_URL
from ..forms import CommentForm


@flask_app.post("/comments/delete/<int:id>")
def delete_comment(id):
    token = request.cookies.get("token")

    if not token:
        flash("You need to log in to delete a comment!", "danger")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}

    response = delete(
        f"{BACKEND_URL}/comments/{id}",
        headers=headers,
    )

    if response.status_code == 204:
        flash("Comment deleted successfully!", "success")
    else:
        flash(f"Error deleting comment: {response.json()}", "danger")
    return redirect(url_for("see_one_post", id=id))


@flask_app.get("/comments/edit/<int:id>")
def edit_comment_page(id):
    resp = get(f"{BACKEND_URL}/comments/{id}")
    if resp.status_code == 200:
        form = CommentForm()
        return render_template("edit_comment.html", form=form, comment_id=id)
    else:
        flash(resp.json(), "danger")
        return redirect(url_for("index"))


@flask_app.post("/comments/edit/<int:id>")
def edit_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data


        token = request.cookies.get("token")

        if not token:
            flash("You need to log in to edit a comment!", "danger")
            return redirect(url_for("login"))

        headers = {"Authorization": f"Bearer {token}"}

        response = put(
            f"{BACKEND_URL}/comments/{id}",
            headers=headers,
            json={
                "content": content,
            },
        )

        if response.status_code == 200:
            flash("Comment edited successfully!", "success")
            return redirect(url_for("see_one_post", id=id))
        else:
            flash(
                f"There was an issue editing the comment. {response.json()}", "danger"
            )
            return redirect(url_for("edit_comment_page", id=id))
    else:
        flash("Form validation failed. Please try again.", "danger")
        return redirect(url_for("edit_comment_page", id=id))
