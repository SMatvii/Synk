from .db import migrate
from .routes import app, post_router


app.include_router(post_router)
