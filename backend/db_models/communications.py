import datetime
from typing import Optional
from database import Base
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func


class Communications(Base):
    __tablename__ = "communications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    message_objectives: Mapped[str]
    delivery_platforms: Optional[Mapped[str]]
    format: Optional[Mapped[str]]
    key_points: Optional[Mapped[str]]
    contents: Optional[Mapped[str]]
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    project_data: Mapped["CommunicationProjectData"] = relationship(
        "CommunicationProjectData"
    )
    indicators: Mapped["CommunicationIndicators"] = relationship(
        "CommunicationIndicators"
    )


class CommunicationProjectData(Base):
    __tablename__ = "communication_project_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    communication_id: Mapped[int] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE")
    )
    objective_id: Mapped[int] = mapped_column(
        ForeignKey("project_data.id", ondelete="CASCADE")
    )
    audience_id: Mapped[int] = mapped_column(
        ForeignKey("project_data.id", ondelete="CASCADE")
    )


class CommunicationIndicators(Base):
    __tablename__ = "communication_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    communication_id: Mapped[int] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE")
    )
    indicator_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change_indicators.id", ondelete="CASCADE")
    )
