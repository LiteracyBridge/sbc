"""add toc indicator to activites table

Revision ID: fb9be496010a
Revises: f13e9ff54be3
Create Date: 2023-06-01 09:56:30.428118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fb9be496010a"
down_revision = "f13e9ff54be3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "activities",
        sa.Column(
            "toc_indicator_id",
            sa.Integer(),
            sa.ForeignKey("theory_of_change_indicators.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("activities", "toc_indicator_id")
