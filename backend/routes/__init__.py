from fastapi import FastAPI

app = FastAPI()

from .post import post_router
from .user import user_router