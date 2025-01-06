from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session


from ..db import User, get_session
from ..schemas import UserModel


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserModel, session: Annotated[Session, Depends(get_session)]):
    user = User(**data.model_dump())
    session.add(user)
    return user
