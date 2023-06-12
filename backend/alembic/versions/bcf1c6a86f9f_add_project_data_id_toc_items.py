"""add project_data_id toc items

Revision ID: bcf1c6a86f9f
Revises: 18baa18af38e
Create Date: 2023-06-12 20:00:50.353427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bcf1c6a86f9f"
down_revision = "18baa18af38e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "theories_of_change_item",
        sa.Column("project_data_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "theory_of_change_items_project_data_id_fkey",
        "theories_of_change_item",
        "project_data",
        ["project_data_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "theory_of_change_items_project_data_id_fkey",
        "theories_of_change_item",
        type_="foreignkey",
    )
    op.drop_column("theories_of_change_item", "project_data_id")
