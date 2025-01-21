from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .config import Config
from .mixins import PKMixin

Base = Config.BASE


class Subscribe(PKMixin, Base):
    __tablename__ = "subscriptions"

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscribed_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    subscriber: Mapped["User"] = relationship(
        foreign_keys=[subscriber_id], back_populates="subscriptions"
    )
    subscribed_to: Mapped["User"] = relationship(
        foreign_keys=[subscribed_to_id], back_populates="subscribers"
    )
