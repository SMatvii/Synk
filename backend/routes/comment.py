from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session


from ..db import Post, Comment, get_session
from ..schemas import CommentModel


comment_router = APIRouter(prefix="/comments", tags=["Comments"])


@comment_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_comment(
    data: CommentModel, session: Annotated[Session, Depends(get_session)]
):
    comment = Comment(**data.model_dump())
    session.add(comment)
    return comment


@comment_router.get("/{post_id}", status_code=status.HTTP_200_OK)
def get_comments_for_post(post_id: int, session: Annotated[Session, Depends(get_session)]):
    
    comments = session.scalars(select(Comment).where(Comment.post_id == post_id)).all()
    if not comments:
        raise HTTPException(status_code=404, detail=f"No comments found for post with id {post_id}")
    return comments


@comment_router.put("/update/{comment_id}")
def update_comment(
    data: CommentModel,
    comment_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    comment = session.scalar(select(Comment).where(Comment.id == comment_id))

    if not comment:
        raise HTTPException(
            status_code=404, detail=f"Comment with id {comment_id} not found"
        )
    post_update = (
        update(Comment).where(Comment.id == comment_id).values(**data.model_dump())
    )
    session.execute(post_update)
    session.commit()
    return {"detail": f"Comment with id {comment_id} updated successfully"}


@comment_router.delete("/delete/{comment_id}")
def delete_comment(comment_id: int, session: Annotated[Session, Depends(get_session)]):
    comment = session.scalar(select(Comment).where(Comment.id == comment_id))
    if not comment:
        raise HTTPException(
            status_code=404, detail=f"Comment with id {comment_id} not found"
        )
    session.delete(comment)
    session.commit()
    return {"detail": f"Comment with id {comment_id} deleted successfully"}


@comment_router.delete("/delete_all/{post_id}")
def delete_all_post_comments(
    post_id: int, session: Annotated[Session, Depends(get_session)]
):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(status_code=404, detail=f"No post with id {post_id}")

    session.execute(delete(Comment).where(Comment.post_id == post_id))
    session.commit()
    return {
        "detail": f"All comments of the post with id {post_id} have been deleted successfully"
    }
