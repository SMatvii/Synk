from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session


from ..db import Post, get_session
from ..schemas import PostModel


post_router = APIRouter(prefix="/posts", tags=["Posts"])

@post_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(data: PostModel, session:Annotated[Session, Depends(get_session)]):
    post = Post(**data.model_dump())
    session.add(post)
    return post