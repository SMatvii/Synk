from pydantic import BaseModel, Field, EmailStr, field_validator
from sqlalchemy import select
from fastapi import HTTPException

from ..db import Config, User
from .hash import get_password_hash

Session = Config.SESSION
        

class EditUserModel(BaseModel):
    name: str = Field(..., description="Username")
    bio: str = Field(default_factory="",description="User bio",max_length=50)


class UserModel(EditUserModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")
    
    @field_validator("email")
    @classmethod
    def check_email(cls, v):
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.email == v))
            if user:
                raise HTTPException(
                    status_code=400, detail="User with this email exists"
                )
            return v

    @field_validator("name")
    @classmethod
    def check_name(cls, v):
        with Session.begin() as session:
            user = session.scalar(select(User).where(User.name == v))
            if user:
                raise HTTPException(
                    status_code=400, detail="User with this name exists"
                )
            return v
        
    @field_validator("password")
    @classmethod
    def hash_psw(cls, v):
        return get_password_hash(v)