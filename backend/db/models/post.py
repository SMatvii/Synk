from typing import List

from .config import Config
from .mixins import PUBMixin,PKMixin

from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import ForeignKey


Base = Config.BASE


class Post(PKMixin,Base,PUBMixin):
    __tablename__ = "posts"

    title:Mapped[str]
    content:Mapped[str]

    user:Mapped["User"] = relationship(back_populates="posts")
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))

    comments:Mapped[List["Comment"]] = relationship(back_populates="post")