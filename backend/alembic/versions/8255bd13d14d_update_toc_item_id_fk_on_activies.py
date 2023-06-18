"""update toc_item_id fk on activies

Revision ID: 8255bd13d14d
Revises: 1fd4d2725491
Create Date: 2023-06-18 11:09:25.955302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8255bd13d14d'
down_revision = '1fd4d2725491'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('activities_toc_item_id_fkey', 'activities', type_='foreignkey')
    op.drop_column('activities', 'toc_item_id')

    # Recreate the column with the correct foreign key
    op.add_column('activities', sa.Column('theory_of_change_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        "activities_theory_of_change_id_fkey",
        "activities",
        "theory_of_change",
        ["theory_of_change_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint('activities_theory_of_change_id_fkey', 'activities', type_='foreignkey')
    op.drop_column('activities', 'theory_of_change_id')

    # Recreate the column with the correct foreign key
    op.add_column('activities', sa.Column('toc_item_id', sa.Integer(), nullable=True))
