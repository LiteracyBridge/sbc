"""create access rquest table

Revision ID: dbf45c06554f
Revises: 976c053d0d61
Create Date: 2023-06-21 17:49:38.468508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dbf45c06554f"
down_revision = "976c053d0d61"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "access_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            onupdate=sa.sql.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            onupdate=sa.sql.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("access_requests")
