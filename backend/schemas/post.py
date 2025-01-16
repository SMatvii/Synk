from pydantic import BaseModel, Field

from ..db import Config


Session = Config.SESSION


class PostModel(BaseModel):
    title: str = Field(max_length=20)
    content: str
