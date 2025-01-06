from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from fastapi import HTTPException

from ..db import Config, User, Post

Session = Config.SESSION


class CommentModel(BaseModel):
    content: str = Field(..., max_length=150, description="Comment content")
    post_id: int
    user_id: int

    @field_validator("user_id")
    @classmethod
    def check_user_id(cls, v):
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.id == v))
            if user:
                return v
            else:
                raise HTTPException(status_code=404, detail=f"No user with this id:{v}")

    @field_validator("post_id")
    @classmethod
    def check_post_id(cls, v):
        with Session.begin() as session:
            post = session.scalar(select(Post).where(Post.id == v))
            if post:
                return v
            else:
                raise HTTPException(status_code=404, detail=f"No user with this id:{v}")