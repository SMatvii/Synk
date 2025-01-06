from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session


from ..db import Comment, get_session
from ..schemas import CommentModel


comment_router = APIRouter(prefix="/comments", tags=["Comments"])

@comment_router.post("/add_comment", status_code=status.HTTP_201_CREATED)
def create_comment(data: CommentModel, session:Annotated[Session, Depends(get_session)]):
    comment = Comment(**data.model_dump())
    session.add(comment)
    return comment