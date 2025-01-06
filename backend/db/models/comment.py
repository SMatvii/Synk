from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .config import Config
from .mixins import PUBMixin, PKMixin


Base = Config.BASE


class Comment(PKMixin, Base, PUBMixin):
    __tablename__ = "comments"

    content: Mapped[str]

    post: Mapped["Post"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship(back_populates="comments")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
