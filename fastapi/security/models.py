from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from security.schemas import Role


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(default="user")
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, comment="UTC date and time"
    )
