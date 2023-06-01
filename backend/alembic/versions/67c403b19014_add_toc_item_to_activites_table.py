"""add toc item to activites table

Revision ID: 67c403b19014
Revises: f13e9ff54be3
Create Date: 2023-06-01 14:25:44.510860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "67c403b19014"
down_revision = "f13e9ff54be3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "activities",
        sa.Column(
            "toc_item_id",
            sa.Integer(),
            sa.ForeignKey("theories_of_change_item.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("activities", "toc_item_id")
