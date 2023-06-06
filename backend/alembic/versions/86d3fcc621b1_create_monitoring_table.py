"""create monitoring table

Revision ID: 86d3fcc621b1
Revises: 5a3efc7e6ff6
Create Date: 2023-06-06 06:24:32.734940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "86d3fcc621b1"
down_revision = "5a3efc7e6ff6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "monitoring",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target", sa.Integer(), nullable=True),
        sa.Column("baseline", sa.Integer(), nullable=True),
        sa.Column("progress", sa.Integer(), nullable=True),
        sa.Column("data_collection_period", sa.String(), nullable=True),
        sa.Column("evaluation", sa.JSON(), nullable=True, server_default="{}"),
        sa.Column("toc_item_indicator_id", sa.Integer(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["toc_item_indicator_id"],
            ["theory_of_change_indicators.id"],
            name="fk_monitoring_toc_item_indicator_id",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="fk_monitoring_project_id",
        ),
    )


def downgrade() -> None:
    op.drop_table("monitoring")
