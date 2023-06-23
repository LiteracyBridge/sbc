"""add evaludation strategy to projects

Revision ID: ef4c710286c6
Revises: e840d0cce468
Create Date: 2023-06-23 08:21:18.576302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ef4c710286c6"
down_revision = "e840d0cce468"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "projects", sa.Column("evaluation_strategy", sa.String(), nullable=True)
    )
    op.add_column(
        "projects", sa.Column("feedback_strategy", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("projects", "evaluation_strategy")
    op.drop_column("projects", "feedback_strategy")
