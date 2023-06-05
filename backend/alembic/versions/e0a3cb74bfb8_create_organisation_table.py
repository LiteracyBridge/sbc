"""Create Organisation table

Revision ID: e0a3cb74bfb8
Revises: 67c403b19014
Create Date: 2023-06-05 06:11:23.192016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e0a3cb74bfb8"
down_revision = "67c403b19014"
branch_labels = None
depends_on = None


# Upgrade function
def upgrade():
    op.create_table(
        "organisations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["lu_countries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


# Downgrade function
def downgrade():
    op.drop_table("organisations")
