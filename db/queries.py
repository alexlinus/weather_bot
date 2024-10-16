from __future__ import annotations

from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from db.subscriber import Subscriber


class SubscriberQueryRepo:
    """Encapsulates queries to Subscriber table."""
    model = Subscriber

    def __init__(self, session: Session):
        self.session: Session = session

    def get_subscriber(self, telegram_id: int) -> Subscriber | None:
        sql_statement = select(self.model).where(self.model.telegram_id == telegram_id)
        result = self.session.execute(sql_statement)
        return result.scalars().first()

    def create_subscriber(self, telegram_id: int, first_name: str, last_name: str) -> None:
        sql_statement = insert(self.model).values(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
        )
        self.session.execute(sql_statement)
        self.session.commit()

    def get_all_subscribers(self) -> Sequence[Subscriber]:
        sql_statement = select(self.model).order_by(Subscriber.created_at)
        result = self.session.execute(sql_statement)
        return result.scalars().all()