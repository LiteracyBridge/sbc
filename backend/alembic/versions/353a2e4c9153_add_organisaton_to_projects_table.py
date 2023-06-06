"""add organisaton to projects table

Revision ID: 353a2e4c9153
Revises: d23183232126
Create Date: 2023-06-06 14:35:45.250191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "353a2e4c9153"
down_revision = "d23183232126"
branch_labels = None
depends_on = None


# Upgrade function
def upgrade():
    op.add_column("projects", sa.Column("organisation_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "projects_organisation_id_fkey",
        "projects",
        "organisations",
        ["organisation_id"],
        ["id"],
        ondelete="CASCADE",
    )


# Downgrade function
def downgrade():
    op.drop_constraint("projects_organisation_id_fkey", "projects", type_="foreignkey")
    op.drop_column("projects", "organisation_id")
