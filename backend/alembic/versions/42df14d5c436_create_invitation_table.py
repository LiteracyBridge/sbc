"""Create Invitation table

Revision ID: 42df14d5c436
Revises: e0a3cb74bfb8
Create Date: 2023-06-05 06:11:45.771487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "42df14d5c436"
down_revision = "e0a3cb74bfb8"
branch_labels = None
depends_on = None


# Upgrade function
def upgrade():
    op.create_table(
        "invitations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phoneNumber", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("organisation_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


# Downgrade function
def downgrade():
    op.drop_table("invitations")
