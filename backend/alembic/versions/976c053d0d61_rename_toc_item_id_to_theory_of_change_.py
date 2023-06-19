"""rename toc_item_id to theory_of_change_id on project_data

Revision ID: 976c053d0d61
Revises: 8255bd13d14d
Create Date: 2023-06-19 08:33:52.773611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '976c053d0d61'
down_revision = '8255bd13d14d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('project_data', 'toc_item_id')
    # op.drop_constraint('fk_project_data_toc_item_id', 'project_data', type_='foreignkey')
    op.add_column(
        'project_data',
        sa.Column(
            'theory_of_change_id',
            sa.Integer(),
            sa.ForeignKey('theory_of_change.id'),
            nullable=True,
        )
    )


def downgrade() -> None:
    op.drop_column('project_data', 'theory_of_change_id')
    # op.drop_constraint('project_data_theory_of_change_id_fkey', 'project_data', type_='foreignkey')

    op.add_column(
        'project_data',
        sa.Column(
            'toc_item_id',
            sa.Integer(),
            sa.ForeignKey('theory_of_change.id'),
            nullable=True,
        )
    )
