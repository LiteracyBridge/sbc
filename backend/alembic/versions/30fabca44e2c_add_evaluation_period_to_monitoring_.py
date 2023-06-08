"""add evaluation period to monitoring table

Revision ID: 30fabca44e2c
Revises: 353a2e4c9153
Create Date: 2023-06-08 11:43:18.109335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "30fabca44e2c"
down_revision = "353a2e4c9153"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "monitoring",
        sa.Column(
            "evaluation_period",
            sa.String(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("monitoring", "evaluation_period")
