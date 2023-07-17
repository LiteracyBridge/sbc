from typing import List
from sqlalchemy import event, or_
from sqlalchemy.orm import Session
from models import Activity, TheoryOfChange, TheoryOfChangeIndicator, Risk
from datetime import datetime


@event.listens_for(TheoryOfChange, "after_insert")
def toc_created(mapper, connection, target: TheoryOfChange):
    "listen for the 'after_insert' event"

    # TODO: create associated activity
    print(target.id)
    # ... (event handling logic) ...


def delete_theory_of_change(item: TheoryOfChange, db: Session):
    """Handle deletion of theory of change related items deletion"""

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
        indicator.delete()

    item.delete()
    db.commit()


def delete_activity(
    item: Activity,
    db: Session,
) -> Activity:
    """Handle deletion of activity related items deletion"""

    # Delete associated theory of change, if any
    if item.theory_of_change_id is not None:
        toc = (
            db.query(TheoryOfChange)
            .filter(TheoryOfChange.id == item.theory_of_change_id)
            .first()
        )
        delete_theory_of_change(toc, db)

    # Delete associated tasks, if parent activity
    if item.parent_id is not None and item.parent_id != 0:
        children = db.query(Activity).filter(Activity.parent_id == item.id).all()

        for child in children:
            child.delete()

    item.delete()
    db.commit()

    return item
