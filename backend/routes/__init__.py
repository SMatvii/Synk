from fastapi import FastAPI

app = FastAPI()

from .comment import comment_router
