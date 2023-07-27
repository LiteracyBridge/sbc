"""add timestamps to project-data

Revision ID: 79cfd77193f1
Revises: df353db51cab
Create Date: 2023-07-27 07:36:13.364918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79cfd77193f1"
down_revision = "df353db51cab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "project_data",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "project_data",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "project_data",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "project_data",
        sa.Column(
            "deleted_by_id",
            sa.Integer(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("project_data", "deleted_by_id")
    op.drop_column("project_data", "deleted_at")
    op.drop_column("project_data", "updated_at")
    op.drop_column("project_data", "created_at")
