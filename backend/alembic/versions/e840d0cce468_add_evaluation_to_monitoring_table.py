"""add evaluation to monitoring table

Revision ID: e840d0cce468
Revises: dbf45c06554f
Create Date: 2023-06-23 05:27:59.259804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e840d0cce468"
down_revision = "dbf45c06554f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "monitoring",
        sa.Column("evaluation", sa.JSON, nullable=True, default=[]),
    )


def downgrade() -> None:
    op.drop_column("monitoring", "evaluation")
