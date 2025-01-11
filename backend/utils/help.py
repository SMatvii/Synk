from os import getenv
from typing import Annotated

from sqlmodel import select, Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError

from ..db import User, get_session, Subscribe
from ..schemas import Token


load_dotenv()

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def get_current_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
    session: Annotated[Session, Depends(get_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = Token(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = session.scalar(select(User).where(User.name == token_data.username))
    if user is None:
        raise credentials_exception
    return user


def find_user_by_id(session, user_id):
    return session.scalar(select(User).where(User.id == user_id))


def is_already_subscribed(session, subscriber_id, subscribed_to_id):
    return session.scalar(
        select(Subscribe).where(
            Subscribe.subscriber_id == subscriber_id,
            Subscribe.subscribed_to_id == subscribed_to_id
        )
    )