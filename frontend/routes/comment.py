from requests import get, post, put, delete
from flask import render_template, redirect, flash, url_for, request
from .. import flask_app, BACKEND_URL


@flask_app.post("/comments/create")
def create_comment(post_id:int, content:str):
    data = {
        "content": content,
        "post_id": post_id
    }
    token = request.cookies.get("token")
    if not token:
        flash("You need to log in to create a comment!", "danger")
        return redirect(url_for("login")) 
    
    headers = {"Authorization": f"Bearer {token}"}
    response = post(f"{BACKEND_URL}/comments", json=data, headers=headers)
    if response.status_code == 201:
        flash("Comment created")
        return redirect(url_for("see_one_post", id=post_id))
    else:
        flash(f"Error creating comment: {response.json()}")
        return redirect(url_for("see_one_post", id=post_id))


