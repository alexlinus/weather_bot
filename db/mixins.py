from datetime import datetime

from sqlalchemy import BIGINT, func, TIMESTAMP, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, declared_attr
from typing import Annotated


class TableNameMixin:

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class TimestampMixing:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=True,
        default=None,
        onupdate=func.now(),
    )


str_255 = Annotated[str, mapped_column(VARCHAR(255), default="")]

