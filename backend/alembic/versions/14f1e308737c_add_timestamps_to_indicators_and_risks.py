"""add timestamps to indicators and risks

Revision ID: 14f1e308737c
Revises: 794131366f67
Create Date: 2023-07-15 07:54:14.481753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "14f1e308737c"
down_revision = "794131366f67"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "risks",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "risks",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "risks", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )

    op.add_column(
        "theory_of_change_indicators",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "theory_of_change_indicators",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "theory_of_change_indicators",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("theory_of_change_indicators", "deleted_at")
    op.drop_column("theory_of_change_indicators", "updated_at")
    op.drop_column("theory_of_change_indicators", "created_at")

    op.drop_column("risks", "deleted_at")
    op.drop_column("risks", "updated_at")
    op.drop_column("risks", "created_at")
