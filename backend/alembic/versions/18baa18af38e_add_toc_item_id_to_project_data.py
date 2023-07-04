"""add toc_item_id to project_data

Revision ID: 18baa18af38e
Revises: 30fabca44e2c
Create Date: 2023-06-12 06:29:18.056749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "18baa18af38e"
down_revision = "30fabca44e2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("project_data", sa.Column("module", sa.String(), nullable=True))
    op.add_column("project_data", sa.Column("name", sa.String(), nullable=True))

    op.add_column(
        "project_data", sa.Column("theory_of_change_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "fk_project_data_theory_of_change_id",
        "project_data",
        "theory_of_change_item",
        ["theory_of_change_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_project_data_theory_of_change_id", "project_data", type_="foreignkey"
    )
    op.drop_column("project_data", "theory_of_change_id")
    op.drop_column("project_data", "name")
    op.drop_column("project_data", "module")
