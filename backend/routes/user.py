from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session


from ..db import User, get_session
from ..schemas import UserModel


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/registrate", status_code=status.HTTP_201_CREATED)
def registrate_user(data: UserModel, session: Annotated[Session, Depends(get_session)]):
    user = User(**data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@user_router.get("/get/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/update/{id}", status_code=status.HTTP_200_OK)
def update_user(id: int, data: UserModel, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in data.model_dump().items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user

@user_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}
