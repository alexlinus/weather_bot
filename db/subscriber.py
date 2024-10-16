from typing import Optional

from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.mixins import TableNameMixin, TimestampMixing, str_255


class Subscriber(Base, TimestampMixing, TableNameMixin):
    """Model to store subscribers data."""
    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        nullable=False,
        autoincrement=False,
    )

    first_name: Mapped[str_255]
    last_name: Mapped[Optional[str_255]]