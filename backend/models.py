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
    group_id: Mapped[int] = mapped_column(
        ForeignKey("lu_indicator_types.id")
    )

    group: Mapped["IndicatorType"] = relationship(
        "IndicatorType", back_populates="indicators",
    )
    theory_of_change: Mapped["TheoryOfChangeIndicator"] = relationship(
        "TheoryOfChangeIndicator", back_populates="indicator",
    )

    # TODO: Generate alembic migration to create a table using the sqlalchemy model below


class TheoryOfChangeIndicator(Base):
    __tablename__ = "theory_of_change_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    theory_of_change_id: Mapped[int] = mapped_column(ForeignKey("toc.id"))
    indicatory_id: Mapped[int] = mapped_column(ForeignKey("lu_indicators.id"))

    indicator = relationship(
        "Indicator", back_populates="theory_of_change", load_on_pending=True
    )

Base.metadata.create_all(bind=engine)


# # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
