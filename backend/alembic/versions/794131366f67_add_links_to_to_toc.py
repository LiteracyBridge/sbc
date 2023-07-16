"""add links-to to toc

Revision ID: 794131366f67
Revises: 38defd1a195a
Create Date: 2023-07-15 07:07:46.244500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "794131366f67"
down_revision = "38defd1a195a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "theory_of_change",
        sa.Column("links_to", sa.ARRAY(sa.Integer()), nullable=True, default=[]),
    )


def downgrade() -> None:
    op.drop_column("theory_of_change", "links_to")
