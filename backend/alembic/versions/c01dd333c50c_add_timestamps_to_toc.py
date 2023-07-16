"""add timestamps to toc

Revision ID: c01dd333c50c
Revises: c0c570901e80
Create Date: 2023-07-04 05:39:02.513941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c01dd333c50c'
down_revision = 'c0c570901e80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "theory_of_change",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "theory_of_change",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "theory_of_change", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "theory_of_change",
        sa.Column(
            "deleted_by_id",
            sa.Integer(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "theory_of_change_deleted_by_id_fkey",
        "theory_of_change",
        "users",
        ["deleted_by_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_column("theory_of_change", "deleted_by_id")
    op.drop_column("theory_of_change", "deleted_at")
    op.drop_column("theory_of_change", "updated_at")
    op.drop_column("theory_of_change", "created_at")
