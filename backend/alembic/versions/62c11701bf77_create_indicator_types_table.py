"""create indicator types table

Revision ID: 62c11701bf77
Revises:
Create Date: 2023-05-18 11:34:01.096910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62c11701bf77"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "lu_indicator_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["lu_indicator_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("lu_indicator_types")
