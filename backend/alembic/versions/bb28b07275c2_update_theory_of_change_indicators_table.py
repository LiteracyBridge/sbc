"""update theory of change indicators table

Revision ID: bb28b07275c2
Revises: a5e9f7f40edb
Create Date: 2023-06-15 06:07:18.601591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb28b07275c2'
down_revision = 'a5e9f7f40edb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('theory_of_change_indicators', 'toc_item_id')
    op.drop_column('theory_of_change_indicators', 'indicator_id')

    op.add_column(
        'theory_of_change_indicators',
        sa.Column('indicator_id', sa.Integer(), nullable=True),
    )
    op.add_column(
        'theory_of_change_indicators',
        sa.Column('theory_of_change_id', sa.Integer(), nullable=False),
    )
    op.add_column(
        'theory_of_change_indicators',
        sa.Column('project_id', sa.Integer(), nullable=False),
    )
    op.add_column(
        'theory_of_change_indicators',
        sa.Column('activity_id', sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        'fk_toc_indicators_theory_of_change_id_toc',
        'theory_of_change_indicators',
        'theory_of_change',
        ['theory_of_change_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_toc_indicators_project_id_projects',
        'theory_of_change_indicators',
        'projects',
        ['project_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_theory_of_change_indicators_activity_id_activities',
        'theory_of_change_indicators',
        'activities',
        ['activity_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_theory_of_change_indicators_indicator_id_indicators',
        'theory_of_change_indicators',
        'indicators',
        ['indicator_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_table("theory_of_change_indicators")
