from typing import Dict, List, Optional
from sqlalchemy import (
    JSON,
    DateTime,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func
from sqlalchemy_easy_softdelete.mixin import generate_soft_delete_mixin_class
from datetime import datetime
from database import Base, SessionLocal, engine


# Create a Class that inherits from our class builder
class SoftDeleteMixin(generate_soft_delete_mixin_class()):
    deleted_at: datetime


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
    indicator_level: Mapped[ARRAY] = mapped_column(ARRAY(String))


class LuImportance(Base):
    __tablename__ = "lu_importance"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    sequence: Mapped[int]
    color: Mapped[Optional[str]]


class LuTheoryOfChangeType(Base):
    __tablename__ = "lu_toc_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


class LuCountries(Base):
    __tablename__ = "lu_countries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]


class Organisation(Base):
    __tablename__ = "organisations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey("lu_countries.id"))

    users: Mapped[List["User"]] = relationship(
        "User", back_populates="organisation", load_on_pending=True
    )


class Invitation(Base):
    __tablename__ = "invitations"
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    email: Mapped[str]
    phoneNumber: Mapped[Optional[str]]
    status: Mapped[str]
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))

    organisation: Mapped["Organisation"] = relationship("Organisation")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    address_as: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    sms: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    whatsapp: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))
    last_project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))

    organisation: Mapped["Organisation"] = relationship(
        "Organisation", back_populates="users"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    evaluation_strategy: Mapped[Optional[str]]
    feedback_strategy: Mapped[Optional[str]]
    sustainability_strategy: Mapped[Optional[str]]
    archived: Mapped[bool] = mapped_column(Boolean, default=False)
    start_date: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    country_id: Mapped[int] = mapped_column(ForeignKey("lu_countries.id"))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))

    # Relations
    stakeholders: Mapped[List["Stakeholder"]] = relationship(
        "Stakeholder", back_populates="project"
    )


class ProjectData(Base):
    __tablename__ = "project_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Question id
    q_id: Mapped[Optional[int]]
    data: Mapped[Optional[str]]

    # Module of data/question -> driver/objective/background_context
    module: Mapped[Optional[str]]

    # Module of data/question -> specific_objectives/behavior_influence
    name: Mapped[Optional[str]]

    prj_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=True)
    editing_user_id: Mapped[int] = mapped_column(ForeignKey("project_users.id"))
    theory_of_change_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id", ondelete="CASCADE"), nullable=True
    )

    project = relationship("Project")


class ProjectUser(Base):
    __tablename__ = "project_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prj_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    editing_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    project = relationship("Project")
    # TODO: add access_id


class LuIntervention(Base):
    __tablename__ = "lu_interventions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    url_description: Mapped[Optional[str]]
    text_short: Mapped[Optional[str]]
    sequence: Mapped[int]


class LuActivityStatus(Base):
    __tablename__ = "lu_activity_status"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    sequence: Mapped[int]


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


class IndicatorType(Base):
    __tablename__ = "lu_indicator_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("lu_indicator_types.id"))

    parent = relationship("IndicatorType", remote_side=[id], load_on_pending=True)
    indicators = relationship("Indicator", back_populates="group")


# TODO: remove this table
class Indicator(Base):
    __tablename__ = "lu_indicators"

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
    # TODO: Generate alembic migration to create a table using the sqlalchemy model below


class ProjectDriver(Base):
    __tablename__ = "drivers_in_prj"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    notes_context: Mapped[Optional[str]]
    notes_gap: Mapped[Optional[str]]
    notes_goal: Mapped[Optional[str]]

    importance_id: Mapped[int] = mapped_column(ForeignKey("lu_importance.id"))
    prj_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    lu_driver_id: Mapped[int] = mapped_column(ForeignKey("lu_drivers.id"))
    editing_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class TheoryOfChange(Base, SoftDeleteMixin):
    __tablename__ = "theory_of_change"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    is_validated: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("lu_toc_types.id"), nullable=True)
    # from_id: Mapped[int] = mapped_column(
    #     ForeignKey("theory_of_change.id"), nullable=True
    # )
    # TODO: remove this field
    # @deprecated
    # to_id: Mapped[int] = mapped_column(ForeignKey("theory_of_change.id"), nullable=True)
    links_to: Mapped[Optional[List]] = mapped_column(
        MutableList.as_mutable(ARRAY(Integer)), nullable=True, default=[]
    )
    sem_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lu_sem.id"), nullable=True
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Related objects
    indicators: Mapped[ARRAY] = relationship(
        "TheoryOfChangeIndicator", back_populates="theory_of_change"
    )
    sem: Mapped["LuSem"] = relationship("LuSem")
    type: Mapped["LuTheoryOfChangeType"] = relationship("LuTheoryOfChangeType")


class ProjectIndicators(Base):
    __tablename__ = "project_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    indi_kit_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lu_indi_kit.id"), nullable=True
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    indi_kit: Mapped["LuIndiKit"] = relationship("LuIndiKit")
    project: Mapped["Project"] = relationship("Project")


class TheoryOfChangeIndicator(Base, SoftDeleteMixin):
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
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    indicator: Mapped["ProjectIndicators"] = relationship("ProjectIndicators")
    theory_of_change: Mapped["TheoryOfChange"] = relationship(
        "TheoryOfChange", back_populates="indicators"
    )
    project: Mapped["Project"] = relationship("Project")


class Risk(Base, SoftDeleteMixin):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    mitigation: Mapped[Optional[str]]
    assumptions: Mapped[Optional[str]]
    risks: Mapped[Optional[str]]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers_in_prj.id"), nullable=True
    )
    toc_from_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id"), nullable=True
    )
    toc_to_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Related objects
    toc_from: Mapped["TheoryOfChange"] = relationship(
        "TheoryOfChange", foreign_keys=[toc_from_id]
    )
    toc_to: Mapped["TheoryOfChange"] = relationship(
        "TheoryOfChange", foreign_keys=[toc_to_id]
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    url: Mapped[Optional[str]]
    notes: Mapped[Optional[str]]

    prj_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    editing_user_id: Mapped[int] = mapped_column(
        ForeignKey("project_users.id"), nullable=True
    )
    theory_of_change_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id"), nullable=True
    )
    parent_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), nullable=True)
    intervention_id: Mapped[int] = mapped_column(
        ForeignKey("lu_interventions.id"), nullable=True
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("project_users.id"), nullable=True)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("lu_activity_status.id"), nullable=True
    )
    driver_ids: Mapped[int] = mapped_column(default=[], nullable=True)
    start_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    end_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Monitoring(Base):
    __tablename__ = "monitoring"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    target: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    baseline: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    progress: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    data_collection_method: Mapped[Optional[str]]
    reporting_period: Mapped[Optional[str]]
    type: Mapped[Optional[str]]
    evaluation: Mapped[ARRAY] = mapped_column(
        MutableList.as_mutable(JSON), nullable=True, default=[]
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    toc_indicator_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change_indicators.id", ondelete="CASCADE"), nullable=True
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    toc_indicator = relationship("TheoryOfChangeIndicator")


class Communication(Base):
    __tablename__ = "communications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    delivery_platforms: Mapped[Optional[str]]
    message_objectives: Mapped[Optional[str]]
    format: Mapped[Optional[str]]
    key_points: Mapped[Optional[str]]
    contents: Mapped[Optional[str]]
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

    drivers: Mapped[ARRAY] = relationship("CommunicationDriver")
    target_audiences: Mapped[ARRAY] = relationship("CommunicationAudience")
    indicators: Mapped[ARRAY] = relationship("CommunicationIndicator")
    project_objectives: Mapped[ARRAY] = relationship("CommunicationObjective")


class CommunicationObjective(Base):
    __tablename__ = "communication_objectives"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    communication_id: Mapped[int] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE")
    )
    objective_id: Mapped[int] = mapped_column(
        ForeignKey("project_data.id", ondelete="CASCADE")
    )


class CommunicationAudience(Base):
    __tablename__ = "communication_audiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    communication_id: Mapped[int] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE")
    )
    audience_id: Mapped[int] = mapped_column(
        ForeignKey("project_data.id", ondelete="CASCADE")
    )


class CommunicationIndicator(Base):
    __tablename__ = "communication_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    communication_id: Mapped[int] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE")
    )
    indicator_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change_indicators.id", ondelete="CASCADE")
    )


class CommunicationDriver(Base):
    __tablename__ = "communication_drivers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    communication_id: Mapped[int] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE")
    )
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers_in_prj.id", ondelete="CASCADE")
    )


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
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Stakeholder(Base, SoftDeleteMixin):
    __tablename__ = "stakeholders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # WhatsApp app number
    whatsapp: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # SMS phone number
    sms: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    editing_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    project: Mapped["Project"] = relationship("Project", back_populates="stakeholders")


Base.metadata.create_all(bind=engine)


# # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
