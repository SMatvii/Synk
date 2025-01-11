from typing import Annotated

from fastapi import Depends, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db import User, get_session, Subscribe
from ..utils import get_current_user, find_user_by_id, is_already_subscribed


subscribe_router = APIRouter(prefix="/sub", tags=["Subscribe"])


@subscribe_router.post("/{subscribe_to_id}")
def subscribe(
    subscribe_to_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_to_subscribe = find_user_by_id(session, subscribe_to_id)

    if not user_to_subscribe:
        return Response("User not found", status_code=404)

    if is_already_subscribed(session, current_user.id, subscribe_to_id):
        return "You are already subscribed to this user"

    subscription = Subscribe(
        subscriber_id=current_user.id, subscribed_to_id=subscribe_to_id
    )
    current = find_user_by_id(session, current_user.id)
    user_to_subscribe.subscribers_count += 1
    current.subscribtions_count += 1
    session.add(subscription)
    return "Subscribed"


@subscribe_router.post("/un/{user_id}")
def unsubscribe(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):

    user_to_unsubscribe = find_user_by_id(session, user_id)

    if not user_to_unsubscribe:
        return Response("User not found", status_code=404)

    subscription = is_already_subscribed(session, current_user.id, user_id)
    if not subscription:
        return "You are not subscribed to this user"

    current = find_user_by_id(session, current_user.id)
    user_to_unsubscribe.subscribers_count -= 1
    current.subscribtions_count -= 1
    session.delete(subscription)
    return "Unsubscribed"


@subscribe_router.get("/subscribers/{user_id}")
def get_user_subscribers(user_id: str, session: Annotated[Session, Depends(get_session)]):
    resp = []
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        return Response("User not found", status_code=404)
    subscriber_ids = session.scalars(select(Subscribe.subscriber_id).where(Subscribe.subscribed_to_id == user.id)).all()

    for id in subscriber_ids:
        subscriber = session.scalar(select(User).where(User.id==id))
        if subscriber:
            resp.append(subscriber)
    return {"subscribers" : resp}


@subscribe_router.get("/subscribtions/{user_id}")
def get_user_subscribtions(user_id: str, session: Annotated[Session, Depends(get_session)]):
    resp = []
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        return Response("User not found", status_code=404)
    subscribtion_ids = session.scalars(select(Subscribe.subscribed_to_id).where(Subscribe.subscriber_id == user.id)).all()
    for id in subscribtion_ids:
        subscribtion = session.scalar(select(User).where(User.id==id))
        if subscribtion:
            resp.append(subscribtion)
    return {"subscribtions" : resp}