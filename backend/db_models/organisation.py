from database import Base, SessionLocal, engine
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import ARRAY, DateTime, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func


class AccessRequest(Base):
    __tablename__ = "access_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    name: Mapped[str]
    notes: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )


Base.metadata.create_all(bind=engine)
