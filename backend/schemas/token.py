from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    email: EmailStr | None = None
