from flask import render_template
from requests import get
from .. import flask_app, BACKEND_URL


@flask_app.get("/posts/<int:id>")
def see_one_post(id):
    post = get(f"{BACKEND_URL}/posts/{id}")
    if post:
        user_id = post.json().get("user_id")
        user = get(f"{BACKEND_URL}/users/{user_id}")
        comments = get(f"{BACKEND_URL}/comments/{id}")
        if comments.status_code == 200: 
            return render_template(
                "post.html", 
                post=post.json(), 
                user=user.json(),
                comments=comments.json()
                )
        else:
            return render_template(
                "post.html", 
                post=post.json(), 
                user=user.json(),
            )


