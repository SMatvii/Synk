from typing import List

from sqlalchemy.orm import Mapped, relationship

from .config import Config
from .mixins import PKMixin


Base = Config.BASE


class User(PKMixin, Base):
    __tablename__ = "users"

    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    posts: Mapped[List["Post"]] = relationship(back_populates="user")

    comments: Mapped[List["Comment"]] = relationship(back_populates="user")