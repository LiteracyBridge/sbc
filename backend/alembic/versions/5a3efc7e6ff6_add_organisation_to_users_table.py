"""add organisation to users table

Revision ID: 5a3efc7e6ff6
Revises: 42df14d5c436
Create Date: 2023-06-05 06:12:37.578603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5a3efc7e6ff6"
down_revision = "42df14d5c436"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("organisation_id", sa.Integer(), nullable=True),
    )
    sa.ForeignKeyConstraint(
        ["organisation_id"],
        ["organisations.id"],
    )


def downgrade() -> None:
    op.drop_column("users", "organisation_id")
    # op.drop_constraint("organisation_id", "users", type_="foreignkey")
