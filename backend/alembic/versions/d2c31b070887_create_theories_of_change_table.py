"""create theories of change table

Revision ID: d2c31b070887
Revises: 6ad7e04413d4
Create Date: 2023-05-22 12:24:21.241697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2c31b070887'
down_revision = '6ad7e04413d4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'theories_of_change',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'])
    )

def downgrade():
    op.drop_table('theories_of_change')
