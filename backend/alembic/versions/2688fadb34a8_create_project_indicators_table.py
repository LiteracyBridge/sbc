"""create project indicators table

Revision ID: 2688fadb34a8
Revises: 88fb801aac56
Create Date: 2023-06-15 05:56:51.698047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2688fadb34a8'
down_revision = '88fb801aac56'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'project_indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('indi_kit_id', sa.Integer(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['indi_kit_id'], ['lu_indi_kit.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    )


def downgrade():
    op.drop_table('project_indicators')
