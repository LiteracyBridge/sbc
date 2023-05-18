"""create theory of change indicators table

Revision ID: 6ad7e04413d4
Revises: e2a28872dea3
Create Date: 2023-05-18 11:39:10.377387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6ad7e04413d4"
down_revision = "e2a28872dea3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "theory_of_change_indicators",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("theory_of_change_id", sa.Integer(), nullable=True),
        sa.Column("indicator_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["theory_of_change_id"],
            ["toc.id"],
        ),
        sa.ForeignKeyConstraint(
            ["indicator_id"],
            ["lu_indicators.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("theory_of_change_indicators")
