"""add theory_of_change to risks table

Revision ID: f13e9ff54be3
Revises: 60ff10fb75b4
Create Date: 2023-05-29 21:40:53.560272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f13e9ff54be3"
down_revision = "60ff10fb75b4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "risks",
        sa.Column(
            "theory_of_change_id",
            sa.Integer(),
            sa.ForeignKey("theories_of_change.id"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("risks", "theory_of_change_id")
