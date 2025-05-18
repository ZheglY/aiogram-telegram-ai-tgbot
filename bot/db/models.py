from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


from sqlalchemy import DateTime

from datetime import datetime



DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)


def current_date():
    """
    Returns the current local date and time without microseconds.

    Returns:
        datetime: The current datetime with microseconds set to 0.
    """
    return datetime.now().replace(microsecond=0)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False, default="en")
    feedback: Mapped[str] = mapped_column(String(2000), nullable=True)
    search_histories = relationship('History', back_populates='user')


class History(Base):
    __tablename__ = "user_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_request: Mapped[str] = mapped_column(String(2000))
    bot_response: Mapped[str] = mapped_column(String(10000))
    date: Mapped[datetime] = mapped_column(DateTime, default=current_date)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"), nullable=False)
    user = relationship('User', back_populates='search_histories')


