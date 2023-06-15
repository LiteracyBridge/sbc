"""create theory of change table

Revision ID: a5e9f7f40edb
Revises: 2688fadb34a8
Create Date: 2023-06-15 06:03:54.250052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5e9f7f40edb"
down_revision = "2688fadb34a8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "theory_of_change",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_validated", sa.Boolean(), nullable=True),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.Column("from_id", sa.Integer(), nullable=True),
        sa.Column("to_id", sa.Integer(), nullable=True),
        sa.Column("sem_id", sa.Integer(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["type_id"], ["lu_toc_types.id"]),
        sa.ForeignKeyConstraint(
            ["from_id"], ["theory_of_change.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["to_id"], ["theory_of_change.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["sem_id"], ["lu_sem.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )


def downgrade():
    op.drop_table("theory_of_change")
