from fastapi import FastAPI

<<<<<<< HEAD
from .routes import comment_router, auth_router, post_router, user_router, upload_router
from .db import migrate, Config, User, Post
=======
from .routes import comment_router, auth_router, post_router, user_router, upload_router, subscribe_router
from .db import migrate
>>>>>>> 15ab731bfd8102f3e2c8f4d53bdda954dc43f064

app = FastAPI()

app.include_router(comment_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(upload_router)
app.include_router(subscribe_router)