from fastapi import FastAPI

app = FastAPI()

from .post import post_router

