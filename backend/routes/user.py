from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from ..db import User, get_session, Post, Comment
from ..schemas import UserModel, UserUpdate


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/registrate", status_code=status.HTTP_201_CREATED)
def registrate_user(data: UserModel, session: Annotated[Session, Depends(get_session)]):
    user = User(**data.model_dump())
    session.add(user)
    return user


@user_router.get("/get/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user


@user_router.put("/update/{id}", status_code=status.HTTP_200_OK)
def update_user(
    id: int, data: UserUpdate, session: Annotated[Session, Depends(get_session)]
):
    user = session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    user_update = update(User).where(User.id == id).values(**data.model_dump())
    session.execute(user_update)
    session.commit()
    return {"detail": f"User with id {id} updated successfully"}


@user_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    session.execute(delete(Comment).where(Comment.user_id == id))

    session.execute(delete(Post).where(Post.user_id == id))

    session.delete(user)

    session.commit()
    return {"detail": f"User with id {id} deleted successfully"}
