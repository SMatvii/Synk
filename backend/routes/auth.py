from typing import Annotated
from datetime import timedelta

from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..db import get_session
from ..schemas import TokenData
from ..utils import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)



auth_router = APIRouter(
    prefix="/auth", tags=["Auth"]
)


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
) -> TokenData:
    """
    Login for access token (first register):

    - **username (name)**: username
    - **password**: password
    - **scope**: optional
    - **client id**: id of client - optional
    - **client secret**: secret of client - optional
    """
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return TokenData(access_token=access_token, token_type="bearer")