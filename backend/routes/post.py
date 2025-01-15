from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session


from ..db import Post, User, get_session, Comment
from ..schemas import PostModel
from ..utils import get_current_user

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostModel,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = Post(**data.model_dump())
    session.add(post)
    return post


@post_router.get("/{post_id}")
def get_one_post(
    post_id: int, 
    session: Annotated[Session, Depends(get_session)]
):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return post


@post_router.get("/users/{user_id}")
def get_users_posts(
    user_id: int, 
    session: Annotated[Session, Depends(get_session)]
):
    resp = []
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id {user_id}"
        )

    posts = session.scalars(select(Post).where(Post.user_id == user_id)).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id {user_id} didn't create any posts",
        )

    for post in posts:
        resp.append(post)

    return resp


@post_router.put("/{post_id}")
def update_post(
    data: PostModel,
    post_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )

    if post.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not creator of this post",
        )

    post_update = update(Post).where(Post.id == post_id).values(**data.model_dump())
    session.execute(post_update)
    session.commit()
    return {"detail": f"Post with id {post_id} updated successfully"}


@post_router.delete("/{post_id}")
def delete_post(
    post_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )

    if post.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not creator of this post",
        )

    session.delete(post)
    session.commit()
    return {"detail": f"Post with id {post_id} deleted successfully"}


@post_router.delete("/users")
def delete_all_user_posts(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    posts = session.scalars(select(Post).where(Post.user_id == current_user.id)).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id {current_user.id} didn't create any posts",
        )

    for post in posts:
        session.execute(delete(Comment).where(Comment.post_id == post.id))
        session.delete(post)

    return {
        "detail": f"All posts by user with id {current_user.id} have been deleted successfully"
    }
