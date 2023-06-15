"""create indikit table

Revision ID: 88fb801aac56
Revises: ca020f717dc4
Create Date: 2023-06-15 05:51:35.635899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88fb801aac56'
down_revision = 'ca020f717dc4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'lu_indi_kit',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('wording_english', sa.String(), nullable=True),
        sa.Column('wording_french', sa.String(), nullable=True),
        sa.Column('wording_portuguese', sa.String(), nullable=True),
        sa.Column('wording_czech', sa.String(), nullable=True),
        sa.Column('guidance', sa.String(), nullable=True),
        sa.Column('section', sa.String(), nullable=True),
        sa.Column('sector', sa.String(), nullable=True),
        sa.Column('sub_sector', sa.String(), nullable=True),
        sa.Column('indicator_level', sa.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('lu_indi_kit')
