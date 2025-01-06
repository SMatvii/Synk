from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column




class PUBMixin:
    pub_date: Mapped[datetime] = mapped_column(default=datetime.now)