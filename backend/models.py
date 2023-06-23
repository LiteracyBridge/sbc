from typing import Dict, List, Optional
from sqlalchemy import (
    ARRAY,
    JSON,
    DateTime,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func

from database import Base, SessionLocal, engine


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

    organisation: Organisation = relationship("Organisation")


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    address_as = Column(String, nullable=True)
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))
    last_project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))

    organisation: Organisation = relationship("Organisation", back_populates="users")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    evaluation_strategy: Mapped[Optional[str]]
    feedback_strategy: Mapped[Optional[str]]
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    start_date: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("lu_countries.id"))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))

    # theories_of_change = relationship(
    #     "TheoryOfChange", back_populates="project", load_on_pending=True
    # )


class ProjectData(Base):
    __tablename__ = "project_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Question id
    q_id: Mapped[Optional[int]]
    data: Mapped[Optional[str]]

    """
    Module of data/question -> driver/objective/background_context
    """
    module: Mapped[Optional[str]]

    """
    Module of data/question -> specific_objectives/behaviour_influence
    """
    name: Mapped[Optional[str]]

    prj_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=True)
    editing_user_id: Mapped[int] = mapped_column(ForeignKey("project_users.id"))
    theory_of_change_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change.id"), nullable=True
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

    description: Mapped[Optional[str]]


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
    # theory_of_change: Mapped["TheoryOfChangeIndicator"] = relationship(
    #     "TheoryOfChangeIndicator",
    #     back_populates="indicator",
    # )

    # TODO: Generate alembic migration to create a table using the sqlalchemy model below


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
    indicators: Mapped[ARRAY["TheoryOfChangeIndicator"]] = relationship(
        "TheoryOfChangeIndicator", back_populates="theory_of_change"
    )
    sem: Mapped["LuSem"] = relationship("LuSem")
    type: Mapped["LuTheoryOfChangeType"] = relationship("LuTheoryOfChangeType")


# TODO: remove this model
class TheoryOfChangeOld(Base):
    __tablename__ = "theories_of_change"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    notes: Mapped[Optional[str]]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    # project = relationship(
    #     "Project", back_populates="theories_of_change", load_on_pending=True
    # )
    # graph = relationship(
    #     "TheoryOfChangeItem", back_populates="theory_of_change", load_on_pending=True
    # )
    # risks = relationship("Risk", load_on_pending=True)


# TODO: remove this model
# class TheoryOfChangeItem(Base):
#     __tablename__ = "theories_of_change_item"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str]
#     description: Mapped[Optional[str]]
#     is_validated: Mapped[bool] = mapped_column(Boolean, default=False)
#     type_id: Mapped[int] = mapped_column(ForeignKey("lu_toc_types.id"), nullable=True)
#     from_id: Mapped[int] = mapped_column(
#         ForeignKey("theories_of_change_item.id"), nullable=True
#     )
#     to_id: Mapped[int] = mapped_column(
#         ForeignKey("theories_of_change_item.id"), nullable=True
#     )
#     sem_id: Mapped[int] = mapped_column(ForeignKey("lu_sem.id"), nullable=True)
#     theory_of_change_id: Mapped[int] = mapped_column(
#         ForeignKey("theories_of_change.id"), nullable=False
#     )
#     project_data_id: Mapped[Optional[int]] = mapped_column(
#         ForeignKey("project_data.id", ondelete="CASCADE"), nullable=True
#     )

#     # todo: add is_validated

#     # Related objects
#     # indicators: Mapped[List["TheoryOfChangeIndicator"]] = relationship(
#     #     "TheoryOfChangeIndicator",
#     # )
#     # theory_of_change = relationship(
#     #     "TheoryOfChange", back_populates="graph", load_on_pending=True
#     # )
#     sem = relationship("LuSem", load_on_pending=True)
#     type = relationship("TheoryOfChangeType", load_on_pending=True)
#     # from_item = relationship(
#     #     "TheoryOfChangeItem",
#     #     remote_side=[to_id],
#     #     foreign_keys=[to_id],
#     #     # back_populates="to_item",
#     #     load_on_pending=True,
#     # )
#     # to_item = relationship(
#     #     "TheoryOfChangeItem",
#     #     # remote_side=[from_id],
#     #     # back_popul//ates="from_item",
#     #     foreign_keys=[from_id],
#     #     load_on_pending=True,
#     # )


# TODO: remove this model
# class TheoryOfChangeIndicator(Base):
#     __tablename__ = "theory_of_change_indicators"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     toc_item_id: Mapped[int] = mapped_column(ForeignKey("theories_of_change_item.id"))
#     indicator_id: Mapped[int] = mapped_column(ForeignKey("lu_indicators.id"))

#     indicator: Mapped["Indicator"] = relationship("Indicator", load_on_pending=True)
#     toc_item: Mapped["TheoryOfChangeItem"] = relationship(
#         "TheoryOfChangeItem", load_on_pending=True, back_populates="indicators"
#     )


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


# TODO: remove this model
# class TheoryOfChangeType(Base):
#     __tablename__ = "lu_toc_types"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str]
#     description: Mapped[Optional[str]]


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
    theory_of_change_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change.id"), nullable=True
    )
    toc_from_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change.id"), nullable=True
    )
    toc_to_id: Mapped[int] = mapped_column(
        ForeignKey("theories_of_change.id"), nullable=True
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


class Monitoring(Base):
    __tablename__ = "monitoring"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    target: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    baseline: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    progress: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    data_collection_method: Mapped[Optional[str]]
    data_collection_frequency: Mapped[Optional[str]]
    evaluation_period: Mapped[Optional[str]]
    evaluation: Mapped[ARRAY] = mapped_column(JSON, nullable=True, default=[])

    toc_indicator_id: Mapped[int] = mapped_column(
        ForeignKey("theory_of_change_indicators.id"), nullable=True
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

    drivers: Mapped[ARRAY["CommunicationDriver"]] = relationship("CommunicationDriver")
    target_audiences: Mapped[ARRAY["CommunicationAudience"]] = relationship(
        "CommunicationAudience"
    )
    indicators: Mapped[ARRAY["CommunicationIndicator"]] = relationship(
        "CommunicationIndicator"
    )
    project_objectives: Mapped[ARRAY["CommunicationObjective"]] = relationship(
        "CommunicationObjective"
    )


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


Base.metadata.create_all(bind=engine)


# # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
