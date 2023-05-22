"""create theories of change items

Revision ID: 70678c95e7cb
Revises: d2c31b070887
Create Date: 2023-05-22 12:39:36.412136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70678c95e7cb'
down_revision = 'd2c31b070887'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'theories_of_change_item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),
        sa.Column('from_id', sa.Integer(), nullable=True),
        sa.Column('to_id', sa.Integer(), nullable=True),
        sa.Column('sem_id', sa.Integer(), nullable=False),
        sa.Column('theory_of_change_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['type_id'], ['lu_toc_types.id']),
        sa.ForeignKeyConstraint(['from_id'], ['theories_of_change_item.id']),
        sa.ForeignKeyConstraint(['to_id'], ['theories_of_change_item.id']),
        sa.ForeignKeyConstraint(['sem_id'], ['lu_sem.id']),
        sa.ForeignKeyConstraint(['theory_of_change_id'], ['theories_of_change.id'])
    )

def downgrade():
    op.drop_table('theories_of_change_item')
