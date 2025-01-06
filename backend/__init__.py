from .db import migrate
from .routes import app, post_router, user_router, comment_router


app.include_router(post_router)
app.include_router(user_router)
app.include_router(comment_router)
