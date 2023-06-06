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


# Upgrade function
def upgrade():
    op.add_column("users", sa.Column("organisation_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "users_organisation_id_fkey",
        "users",
        "organisations",
        ["organisation_id"],
        ["id"],
        ondelete="CASCADE",
    )


# Downgrade function
def downgrade():
    op.drop_constraint("users_organisation_id_fkey", "users", type_="foreignkey")
    op.drop_column("users", "organisation_id")
