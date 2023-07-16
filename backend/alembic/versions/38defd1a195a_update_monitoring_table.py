"""update monitoring table

Revision ID: 38defd1a195a
Revises: 361a95e5ca42
Create Date: 2023-07-08 11:31:07.940997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "38defd1a195a"
down_revision = "361a95e5ca42"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change target and baseline to text
    op.alter_column("monitoring", "target", type_=sa.Text())
    op.alter_column("monitoring", "baseline", type_=sa.Text())
    op.alter_column("monitoring", "progress", type_=sa.Text())

    # Rename evaluation_period to data_collection_method
    op.alter_column(
        "monitoring", "evaluation_period", new_column_name="reporting_period"
    )

    # Add type column
    op.add_column("monitoring", sa.Column("type", sa.String(), nullable=True))
    op.add_column(
        "monitoring",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "monitoring",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "monitoring", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "monitoring",
        sa.Column(
            "deleted_by_id",
            sa.Integer(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "monitoring_deleted_by_id_fkey",
        "monitoring",
        "users",
        ["deleted_by_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("monitoring", "data_collection_frequency")


def downgrade() -> None:
    # Change target and baseline to integer
    op.alter_column("monitoring", "target", type_=sa.Integer())
    op.alter_column("monitoring", "baseline", type_=sa.Integer())

    # Rename data_collection_method to evaluation_period
    op.alter_column(
        "monitoring", "reporting_period", new_column_name="evaluation_period"
    )

    # Remove type column
    op.drop_column("monitoring", "type")
    op.drop_column("monitoring", "created_at")
    op.drop_column("monitoring", "updated_at")
    op.drop_column("monitoring", "deleted_at")
    op.drop_column("activities", "deleted_by_id")

    op.add_column(
        "monitoring",
        sa.Column("data_collection_frequency", sa.String(), nullable=True),
    )
