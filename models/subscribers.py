from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import relationship, mapped_column


def uuid_to_str():
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class Subscriber(Base):
    __tablename__ = 'subscribers'

    id: Mapped[str] = mapped_column(String(200), default=uuid_to_str, primary_key=True)
    user_id: Mapped[int] = Column(Integer, unique=True, nullable=False)
    user_name: Mapped[str] = Column(String(200), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_use: Mapped[datetime] = Column(DateTime)
    prime: Mapped[bool] = Column(Boolean, default=False)
    prime_expire: Mapped[datetime] = Column(DateTime)
    # Foreingkeys

    user_requests: Mapped[List["UserRequest"]] = relationship(back_populates="user")


class UserRequest(Base):
    __tablename__ = 'user_requests'
    id: Mapped[str] = mapped_column(String(200), default=uuid_to_str, primary_key=True)
    text: Mapped[str] = Column(Text, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Foreignkeys
    subscriber_id: Mapped[str] = mapped_column(ForeignKey("subscribers.id"), nullable=False)
    user: Mapped["Subscriber"] = relationship(back_populates="user_requests")


def create_subscriber_table(engine):
    Base.metadata.create_all(engine)