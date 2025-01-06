from datetime import datetime

from pydantic import BaseModel,Field, field_validator
from sqlalchemy import select
from fastapi import HTTPException

from ..db import Config, User


Session=Config.SESSION

class PostModel(BaseModel):
    title:str = Field(max_length=20)
    content:str 
    user_id:int

    @field_validator("user_id")
    @classmethod
    def check_id(cls, v):
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.id==v))
            if user:
                return v
            else:
                raise HTTPException(status_code=404, detail=f"No user with this id:{v}")



