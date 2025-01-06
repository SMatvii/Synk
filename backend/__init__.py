from .db import migrate
from .routes import app, comment_router



app.include_router(comment_router)
