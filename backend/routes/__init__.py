from fastapi import FastAPI

app = FastAPI()

from .user import user_router
