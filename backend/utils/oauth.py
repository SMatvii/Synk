from os import getenv
from typing import Annotated
from datetime import timedelta, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError

from ..db import User, get_session
from ..schemas import Token
from .help import verify_password


load_dotenv()

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(
    email: str,
    password: str,
    session: Annotated[Session, Depends(get_session)],
):
    user = session.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=404, detail="No user with this email")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = Token(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = session.scalar(select(User).where(User.email == token_data.email))
    if user is None:
        raise credentials_exception
    return user
