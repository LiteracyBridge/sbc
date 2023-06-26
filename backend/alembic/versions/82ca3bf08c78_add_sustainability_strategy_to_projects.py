"""add sustainability strategy to projects

Revision ID: 82ca3bf08c78
Revises: ef4c710286c6
Create Date: 2023-06-26 06:56:28.939576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "82ca3bf08c78"
down_revision = "ef4c710286c6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "projects", sa.Column("sustainability_strategy", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("projects", "sustainability_strategy")
