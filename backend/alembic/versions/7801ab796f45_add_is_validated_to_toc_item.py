"""add is-validated to toc item

Revision ID: 7801ab796f45
Revises: 70678c95e7cb
Create Date: 2023-05-25 13:12:56.935457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7801ab796f45"
down_revision = "70678c95e7cb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "theories_of_change_item",
        sa.Column("is_validated", sa.Boolean(), nullable=True, default=False),
    )


def downgrade() -> None:
    op.drop_column("theories_of_change_item", "is_validated")
