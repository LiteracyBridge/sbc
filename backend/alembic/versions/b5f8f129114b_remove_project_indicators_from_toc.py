"""remove project indicators from toc

Revision ID: b5f8f129114b
Revises: 3f5e534a87c7
Create Date: 2023-08-29 15:56:47.467335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b5f8f129114b"
down_revision = "3f5e534a87c7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "theory_of_change_indicators", sa.Column("name", sa.Text(), nullable=True)
    )
    op.add_column(
        "theory_of_change_indicators",
        sa.Column(
            "indikit_id",
            sa.Integer(),
            sa.ForeignKey("lu_indi_kit.id", ondelete="CASCADE"),
            nullable=True,
        ),
    )
    op.drop_column("theory_of_change_indicators", "indicator_id")


def downgrade() -> None:
    op.add_column(
        "theory_of_change_indicators",
        sa.Column(
            "indicator_id",
            sa.Integer(),
            sa.ForeignKey("project_indicators.id", ondelete="CASCADE"),
            nullable=True,
        ),
    )
    op.drop_column("theory_of_change_indicators", "indikit_id")
    op.drop_column("theory_of_change_indicators", "name")
