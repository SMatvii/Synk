from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session


from ..db import Post, Comment, get_session, User
from ..schemas import CommentModel
from ..utils import get_current_user


comment_router = APIRouter(prefix="/comments", tags=["Comments"])


@comment_router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(
    data: CommentModel,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    comment = Comment(**data.model_dump(), user_id=current_user.id)
    session.add(comment)
    return comment


@comment_router.get("/{post_id}", status_code=status.HTTP_200_OK)
def get_comments_for_post(
    post_id: int, session: Annotated[Session, Depends(get_session)]
):
    comments = session.scalars(select(Comment).where(Comment.post_id == post_id)).all()
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No comments found for post with id {post_id}",
        )
    return comments


@comment_router.put("/{comment_id}")
def update_comment(
    data: CommentModel,
    comment_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    comment = session.scalar(select(Comment).where(Comment.id == comment_id))

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the author of this comment",
        )

    comment_update = (
        update(Comment).where(Comment.id == comment_id).values(**data.model_dump())
    )
    session.execute(comment_update)
    session.commit()
    return {"detail": f"Comment with id {comment_id} updated successfully"}


@comment_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    comment = session.scalar(select(Comment).where(Comment.id == comment_id))
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the author of this comment",
        )

    session.delete(comment)
    session.commit()
    return {"detail": f"Comment with id {comment_id} deleted successfully"}


@comment_router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_post_comments(
    post_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {post_id}"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the author of this post",
        )

    session.execute(delete(Comment).where(Comment.post_id == post_id))
    session.commit()
    return {
        "detail": f"All comments of the post with id {post_id} have been deleted successfully"
    }
