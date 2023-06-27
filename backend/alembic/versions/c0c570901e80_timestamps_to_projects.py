"""timestamps to projects

Revision ID: c0c570901e80
Revises: 82ca3bf08c78
Create Date: 2023-06-27 05:17:13.678175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0c570901e80"
down_revision = "82ca3bf08c78"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "projects",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "projects", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "projects",
        sa.Column(
            "deleted_by_id",
            sa.Integer(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "projects_deleted_by_id_fkey",
        "projects",
        "users",
        ["deleted_by_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_column("projects", "deleted_by_id")
    op.drop_column("projects", "deleted_at")
    op.drop_column("projects", "updated_at")
    op.drop_column("projects", "created_at")
