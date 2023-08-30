"""update indikit table

Revision ID: 6af89eddbba1
Revises: b5f8f129114b
Create Date: 2023-08-30 11:42:09.145478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6af89eddbba1"
down_revision = "b5f8f129114b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("lu_indi_kit", sa.Column("purpose", sa.Text(), nullable=True))
    op.add_column("lu_indi_kit", sa.Column("import_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("lu_indi_kit", "purpose")
    op.drop_column("lu_indi_kit", "import_id")
