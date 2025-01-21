from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from ..db import User, get_session, Post, Comment
from ..schemas import EditUserModel, UserModel
from ..utils import get_current_user


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/registrate", status_code=status.HTTP_201_CREATED)
def registrate_user(
    data: UserModel, 
    session: Annotated[Session, Depends(get_session)],
   
):
    user = User(**data.model_dump())
    session.add(user)
    return user


@user_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(
    id: int, 
    session: Annotated[Session, Depends(get_session)]
):
    user = session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


@user_router.put("/", status_code=status.HTTP_200_OK)
def update_user( 
    data: EditUserModel, 
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    user_update = update(User).where(User.id == current_user.id).values(**data.model_dump())
    session.execute(user_update)
    session.commit()
    return {"detail": f"User updated successfully"}


@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    user = session.scalar(select(User).where(User.id == current_user.id))

    session.execute(delete(Comment).where(Comment.user_id == current_user.id))

    user_posts = session.scalars(select(Post).where(Post.user_id==current_user.id))

    for post in user_posts:
        session.execute(delete(Comment).where(Comment.post_id == post.id))
        session.delete(post)

    session.delete(user)

    session.commit()
    return {"detail": f"User with id {current_user.id} deleted successfully"}



@user_router.get("/current_user")
def get_currentuser(current_user: Annotated[User, Depends(get_current_user)],):
    return current_user

 