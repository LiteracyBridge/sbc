"""make toc_item_id optional on activies

Revision ID: 1fd4d2725491
Revises: bb28b07275c2
Create Date: 2023-06-18 11:03:14.378264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fd4d2725491'
down_revision = 'bb28b07275c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('activities', 'toc_item_id', nullable=True)


def downgrade() -> None:
    op.alter_column('activities', 'toc_item_id', nullable=False)
