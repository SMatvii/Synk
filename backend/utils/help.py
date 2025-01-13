from passlib.context import CryptContext
from ..db import User, Subscribe
from sqlalchemy import select

PWD_CONTEXT = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password):
    return PWD_CONTEXT.hash(password)


def find_user_by_id(session, user_id):
    return session.scalar(select(User).where(User.id == user_id))


def is_already_subscribed(session, subscriber_id, subscribed_to_id):
    return session.scalar(
        select(Subscribe).where(
            Subscribe.subscriber_id == subscriber_id,
            Subscribe.subscribed_to_id == subscribed_to_id
        )
    )