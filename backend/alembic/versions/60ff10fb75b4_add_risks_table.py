"""add risks table

Revision ID: 60ff10fb75b4
Revises: 7801ab796f45
Create Date: 2023-05-29 18:41:53.971622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60ff10fb75b4'
down_revision = '7801ab796f45'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'risks',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('risks', sa.String(), nullable=True),
        sa.Column('assumptions', sa.String(), nullable=True),
        sa.Column('mitigation', sa.String(), nullable=True),

        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('driver_id', sa.Integer(), sa.ForeignKey('drivers_in_prj.id'), nullable=True),
        sa.Column('toc_from_id', sa.Integer(), sa.ForeignKey('theories_of_change_item.id'), nullable=True),
        sa.Column('toc_to_id', sa.Integer(), sa.ForeignKey('theories_of_change_item.id'), nullable=True),
    )


def downgrade():
    op.drop_table('risks')
