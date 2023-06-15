from typing import Optional
from database import Base, SessionLocal, engine
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import ARRAY, DateTime, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped


class LuIndiKit(Base):
    __tablename__ = "lu_indi_kit"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    wording_english: Mapped[str]
    wording_french: Mapped[Optional[str]]
    wording_portuguese: Mapped[Optional[str]]
    wording_czech: Mapped[Optional[str]]
    guidance: Mapped[Optional[str]]

    section: Mapped[Optional[str]]
    sector: Mapped[str]
    sub_sector: Mapped[Optional[str]]
    indicator_level: Mapped[ARRAY[str]] = mapped_column(ARRAY(String))


class LuTheoryOfChangeType(Base):
    __tablename__ = "lu_toc_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
