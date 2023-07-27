from typing import List
from sqlalchemy import event, or_
from sqlalchemy.orm import Session
from models import (
    Activity,
    CommunicationObjective,
    ProjectData,
    TheoryOfChange,
    CommunicationIndicator,
    Monitoring,
    TheoryOfChangeIndicator,
    Risk,
    CommunicationAudience,
)
from datetime import datetime


def delete_indicator(toc_indicator_id: int, db: Session):
    """Handle deletion of theory of change indicator related items deletion"""

    # Delete associated indicator records
    indicator = (
        db.query(TheoryOfChangeIndicator)
        .filter(TheoryOfChangeIndicator.id == toc_indicator_id)
        .first()
    )

    if indicator is None:
        return

    # Delete associated monitoring items
    monitoring_items = (
        db.query(Monitoring).filter(Monitoring.toc_indicator_id == indicator.id).all()
    )
    for item in monitoring_items:
        item.delete()

    # Delete associated communication indicators
    communication_indicators = (
        db.query(CommunicationIndicator)
        .filter(CommunicationIndicator.indicator_id == indicator.id)
        .all()
    )
    for item in communication_indicators:
        db.delete(item)

    indicator.delete()
    db.commit()

    return indicator


def delete_theory_of_change(item_id: int, db: Session):
    """Handle deletion of theory of change related items deletion"""

    item = db.query(TheoryOfChange).filter(TheoryOfChange.id == item_id).first()
    if item is None:
        return

    # Remove all associated links_to
    matched_items: List[TheoryOfChange] = (
        db.query(TheoryOfChange)
        .filter(TheoryOfChange.links_to.contains([item.id]))
        .all()
    )
    for toc in matched_items:
        if toc.links_to is not None:
            toc.links_to.remove(item.id)
            toc.links_to = toc.links_to
            toc.updated_at = datetime.now()

            db.commit()

    # Delete associated risk records
    risks = (
        db.query(Risk)
        .filter(
            or_(Risk.toc_from_id == item.id, Risk.toc_to_id == item.id),
        )
        .all()
    )
    for risk in risks:
        risk.delete()

    # Delete associated indicator records
    indicators = (
        db.query(TheoryOfChangeIndicator)
        .filter(TheoryOfChangeIndicator.theory_of_change_id == item.id)
        .all()
    )
    for indicator in indicators:
        delete_indicator(indicator.id, db)
        # indicator.delete()

    item.delete()
    db.commit()


def delete_project_data(item_id: int, db: Session):
    project_data: ProjectData | None = (
        db.query(ProjectData).filter(ProjectData.id == item_id).first()
    )

    if project_data is None:
        return

    # Delete ref theory of change
    if project_data.theory_of_change_id is not None:
        delete_theory_of_change(project_data.theory_of_change_id, db)

    # Delete associated communication audience
    if project_data.module == "audiences":
        audience = (
            db.query(CommunicationAudience)
            .filter(CommunicationAudience.audience_id == item_id)
            .all()
        )
        for item in audience:
            db.delete(item)

    # Delete associated communication objectives
    if project_data.module == "objectives":
        objectives = (
            db.query(CommunicationObjective)
            .filter(CommunicationObjective.objective_id == item_id)
            .all()
        )
        for item in objectives:
            db.delete(item)

    project_data.delete()
    db.commit()

    return project_data


def delete_activity(
    item: Activity,
    db: Session,
) -> Activity:
    """Handle deletion of activity related items deletion"""

    # Delete associated theory of change, if any
    if item.theory_of_change_id is not None:
        delete_theory_of_change(item.theory_of_change_id, db)

    # Delete associated tasks, if parent activity
    if item.parent_id is not None and item.parent_id != 0:
        children = db.query(Activity).filter(Activity.parent_id == item.id).all()

        for child in children:
            child.delete()

    item.delete()
    db.commit()

    return item
