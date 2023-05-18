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


class IndicatoryType(Base):
    __tablename__ = "lu_indicatory_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(ForeignKey("indicatory_types.id"))

    # parent_id = Column(Integer, ForeignKey("indicatory_types.id"))
    # name = Column(String)
    parent: Mapped["IndicatoryType"] = relationship(back_populates="parent")


class Indicators(Base):
    __tablename__ = "lu_indicators"

    # id = Column(Integer, primary_key=True, index=True)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    Phrasing: Mapped[str]
    purpose: Mapped[str]
    link: Mapped[str]
    # name = Column(String)
    # group_id = Column(Integer, ForeignKey("lu_indicatory_types.id"))
    # phrasing = Column(String)
    # purpose = Column(String)
    # link = Column(String)
    group_id: Mapped[int] = mapped_column(ForeignKey("lu_indicatory_types.id"))
    parent: Mapped["IndicatoryType"] = relationship(back_populates="parent")




class TheoryOfChangeIndicators(Base):
    __tablename__ = "theory_of_change_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # id = Column(Integer, primary_key=True, index=True)
    theory_of_change_id = Column(Integer, ForeignKey("toc.id"))
    indicatory_id = Column(Integer, ForeignKey("lu_indicators.id"))


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")

Base.metadata.create_all(bind=engine)


# # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
