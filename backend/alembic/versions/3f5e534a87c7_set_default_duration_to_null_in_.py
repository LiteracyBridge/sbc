"""set default duration to null in activities

Revision ID: 3f5e534a87c7
Revises: 79cfd77193f1
Create Date: 2023-08-29 12:36:00.099234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f5e534a87c7"
down_revision = "79cfd77193f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("activities", "start_date", server_default=None)
    op.alter_column("activities", "end_date", server_default=None)
    pass


def downgrade() -> None:
    pass
