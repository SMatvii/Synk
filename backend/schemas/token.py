from pydantic import BaseModel

class TokenData(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    username: str | None = None