"""add email website and logo to organisations

Revision ID: df353db51cab
Revises: 51fe390d1f8d
Create Date: 2023-07-24 08:41:37.919851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "df353db51cab"
down_revision = "51fe390d1f8d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "organisations", sa.Column("email", sa.String(length=255), nullable=True)
    )
    op.add_column("organisations", sa.Column("logo", sa.Text(), nullable=True))
    op.add_column(
        "organisations", sa.Column("website", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("organisations", "website")
    op.drop_column("organisations", "logo")
    op.drop_column("organisations", "email")
