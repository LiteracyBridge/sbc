"""add timestamps to activities

Revision ID: 361a95e5ca42
Revises: c01dd333c50c
Create Date: 2023-07-07 23:00:17.728188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '361a95e5ca42'
down_revision = 'c01dd333c50c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "activities",
        sa.Column(
            "start_date",
            sa.DateTime(timezone=True),
            nullable=True
        ),
    )
    op.add_column(
        "activities",
        sa.Column(
            "end_date",
            sa.DateTime(timezone=True),
            nullable=True
        ),
    )
    op.add_column(
        "activities",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "activities",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "activities", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "activities",
        sa.Column(
            "deleted_by_id",
            sa.Integer(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "activities_deleted_by_id_fkey",
        "activities",
        "users",
        ["deleted_by_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_column("activities", "deleted_by_id")
    op.drop_column("activities", "end_date")
    op.drop_column("activities", "start_date")
    op.drop_column("activities", "deleted_at")
    op.drop_column("activities", "updated_at")
    op.drop_column("activities", "created_at")
