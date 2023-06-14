"""add start and end date to projects

Revision ID: ca020f717dc4
Revises: bcf1c6a86f9f
Create Date: 2023-06-14 13:21:30.589441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ca020f717dc4"
down_revision = "bcf1c6a86f9f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("start_date", sa.DateTime(), nullable=True))
    op.add_column("projects", sa.Column("end_date", sa.DateTime(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("projects", "end_date")
    op.drop_column("projects", "start_date")
