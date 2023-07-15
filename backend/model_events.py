from sqlalchemy import event
from models import TheoryOfChange


@event.listens_for(TheoryOfChange, "after_insert")
def toc_created(mapper, connection, target: TheoryOfChange):
    "listen for the 'after_insert' event"

    # TODO: create associated activity
    print(target.id)
    # ... (event handling logic) ...

@event.listens_for(TheoryOfChange, "after_delete")
def toc_deleted(mapper, connection, target: TheoryOfChange):
    "listen for the 'after_delete' event"

    # TODO: remove associated activity & links_to
    print(target.id)
    # ... (event handling logic) ...
