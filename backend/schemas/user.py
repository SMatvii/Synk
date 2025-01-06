from pydantic import BaseModel, Field, EmailStr, field_validator
from sqlalchemy import select
from fastapi import HTTPException

from ..db import Config, User

Session = Config.SESSION

class UserModel(BaseModel):
    name: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")

    @field_validator("email")
    @classmethod
    def check_email(cls, v):
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.email==v))
            if user:
                raise HTTPException(status_code=400,detail="User with this email exists")
            return v

        

    