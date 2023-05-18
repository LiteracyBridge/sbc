"""create indicators table

Revision ID: e2a28872dea3
Revises: 62c11701bf77
Create Date: 2023-05-18 11:37:29.101447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e2a28872dea3"
down_revision = "62c11701bf77"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "lu_indicators",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("Phrasing", sa.String(), nullable=True),
        sa.Column("purpose", sa.String(), nullable=True),
        sa.Column("link", sa.String(), nullable=True),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["lu_indicatory_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("lu_indicators")
