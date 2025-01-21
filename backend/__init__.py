from fastapi import FastAPI


from .routes import (
    comment_router,
    auth_router,
    post_router,
    user_router,
    subscribe_router,
)
from .db import migrate, Config, User, Post, Comment


app = FastAPI()

app.include_router(comment_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(subscribe_router)
