"""add feedback strategy to projects table

Revision ID: d23183232126
Revises: 86d3fcc621b1
Create Date: 2023-06-06 06:40:52.179699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d23183232126"
down_revision = "86d3fcc621b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "projects", sa.Column("feedback_strategy", sa.String(), nullable=True)
    )
    op.add_column(
        "projects", sa.Column("evaluation_strategy", sa.JSON(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("projects", "feedback_strategy")
    op.drop_column("projects", "evaluation_strategy")
