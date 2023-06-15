from typing import Optional
from models import LuSem, Project
from .lookups import LuIndiKit, LuTheoryOfChangeType
from database import Base, SessionLocal, engine
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped


class ProjectIndicators(Base):
    __tablename__ = "project_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    indi_kit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lu_indi_kit.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    indi_kit: Mapped["LuIndiKit"] = relationship("LuIndiKit")
    project: Mapped["Project"] = relationship("Project")


class TheoryOfChangeIndicator(Base):
    __tablename__ = "theory_of_change_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    indicator_id: Mapped[int] = mapped_column(
        ForeignKey("project_indicators.id", ondelete="CASCADE")
    )
    theory_of_change_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id", ondelete="CASCADE")
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE")
    )

    indicator: Mapped["ProjectIndicators"] = relationship("ProjectIndicators")
    theory_of_change: Mapped["TheoryOfChange"] = relationship(
        "TheoryOfChange", back_populates="indicators"
    )
    project: Mapped["Project"] = relationship("Project")


class TheoryOfChange(Base):
    __tablename__ = "theory_of_change"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("lu_toc_types.id"), nullable=True)
    from_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id"), nullable=True
    )
    to_id: Mapped[int] = mapped_column(ForeignKey("theory_of_change.id"), nullable=True)
    sem_id: Mapped[int] = mapped_column(ForeignKey("lu_sem.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    # TODO: add risks

    # Related objects
    indicators: Mapped["TheoryOfChangeIndicator"] = relationship(
        "TheoryOfChangeIndicator", back_populates="theory_of_change"
    )
    sem: Mapped["LuSem"] = relationship("LuSem")
    type: Mapped["LuTheoryOfChangeType"] = relationship("LuTheoryOfChangeType")

    # from_item = relationship(
    #     "TheoryOfChangeItem",
    #     remote_side=[to_id],
    #     foreign_keys=[to_id],
    #     # back_populates="to_item",
    #     load_on_pending=True,
    # )
    # to_item = relationship(
    #     "TheoryOfChangeItem",
    #     # remote_side=[from_id],
    #     # back_popul//ates="from_item",
    #     foreign_keys=[from_id],
    #     load_on_pending=True,
    # )
