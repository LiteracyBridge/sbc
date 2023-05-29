from typing import List, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped

from database import Base, SessionLocal, engine


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    address_as = Column(String, nullable=True)

    # is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")


class LuSem(Base):
    __tablename__ = "lu_sem"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


class LuDriver(Base):
    __tablename__ = "lu_drivers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    dgroup: Mapped[str]
    text_short: Mapped[Optional[str]]
    text_long: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    sequence: Mapped[int]

    category_id: Mapped[Optional[int]]
    framework_id: Mapped[Optional[int]]
    intervention_ids: Mapped[int]
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lu_drivers.id"), nullable=True
    )
    sem_id: Mapped[int] = mapped_column(Integer, ForeignKey("lu_sem.id"), nullable=True)

    description: Mapped[Optional[str]]


class IndicatorType(Base):
    __tablename__ = "lu_indicator_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("lu_indicator_types.id"))

    parent = relationship("IndicatorType", remote_side=[id], load_on_pending=True)
    indicators = relationship("Indicator", back_populates="group")


class Indicator(Base):
    __tablename__ = "lu_indicators"

    # id = Column(Integer, primary_key=True, index=True)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    phrasing: Mapped[str]
    purpose: Mapped[str]
    link: Mapped[str]
    group_id: Mapped[int] = mapped_column(ForeignKey("lu_indicator_types.id"))

    group: Mapped["IndicatorType"] = relationship(
        "IndicatorType",
        back_populates="indicators",
    )
    theory_of_change: Mapped["TheoryOfChangeIndicator"] = relationship(
        "TheoryOfChangeIndicator",
        back_populates="indicator",
    )

    # TODO: Generate alembic migration to create a table using the sqlalchemy model below


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    theories_of_change = relationship(
        "TheoryOfChange", back_populates="project", load_on_pending=True
    )


class ProjectDriver(Base):
    __tablename__ = "drivers_in_prj"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    notes_context: Mapped[Optional[str]]
    notes_gap: Mapped[Optional[str]]
    notes_goal: Mapped[Optional[str]]

    prj_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    lu_driver_id: Mapped[int] = mapped_column(ForeignKey("lu_drivers.id"))
    editing_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class TheoryOfChange(Base):
    __tablename__ = "theories_of_change"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    notes: Mapped[Optional[str]]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    project = relationship(
        "Project", back_populates="theories_of_change", load_on_pending=True
    )
    graph = relationship(
        "TheoryOfChangeItem", back_populates="theory_of_change", load_on_pending=True
    )


class TheoryOfChangeItem(Base):
    __tablename__ = "theories_of_change_item"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("lu_toc_types.id"), nullable=True)
    from_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change_item.id"), nullable=True
    )
    to_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change_item.id"), nullable=True
    )
    sem_id: Mapped[int] = mapped_column(ForeignKey("lu_sem.id"), nullable=True)
    theory_of_change_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change.id"), nullable=False
    )

    # todo: add is_validated

    # Related objects
    indicators: Mapped[List["TheoryOfChangeIndicator"]] = relationship(
        "TheoryOfChangeIndicator",
    )
    theory_of_change = relationship(
        "TheoryOfChange", back_populates="graph", load_on_pending=True
    )
    sem = relationship("LuSem", load_on_pending=True)
    type = relationship("TheoryOfChangeType", load_on_pending=True)
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


class TheoryOfChangeIndicator(Base):
    __tablename__ = "theory_of_change_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    toc_item_id: Mapped[int] = mapped_column(ForeignKey("theories_of_change_item.id"))
    indicator_id: Mapped[int] = mapped_column(ForeignKey("lu_indicators.id"))

    indicator: Mapped["Indicator"] = relationship("Indicator", load_on_pending=True)


class TheoryOfChangeType(Base):
    __tablename__ = "lu_toc_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    mitigation: Mapped[Optional[str]]
    assumptions: Mapped[Optional[str]]
    risks: Mapped[Optional[str]]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=True)
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers_in_prj.id"), nullable=True
    )
    toc_from_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change_item.id"), nullable=True
    )
    toc_to_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change_item.id"), nullable=True
    )


Base.metadata.create_all(bind=engine)


# # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
