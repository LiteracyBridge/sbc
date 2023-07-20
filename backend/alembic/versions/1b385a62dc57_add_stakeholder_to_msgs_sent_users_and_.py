"""add stakeholder to msgs_sent_users and msgs_received

Revision ID: 1b385a62dc57
Revises: 14f1e308737c
Create Date: 2023-07-20 07:36:58.966424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b385a62dc57"
down_revision = "14f1e308737c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("msgs_sent_users", "user_id", nullable=True)
    op.alter_column("msgs_received", "user_id", nullable=True)

    op.add_column(
        "msgs_sent_users", sa.Column("stakeholder_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "msgs_sent_users_stakeholder_id_fkey",
        "msgs_sent_users",
        "stakeholders",
        ["stakeholder_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.add_column(
        "msgs_received", sa.Column("stakeholder_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "msgs_received_stakeholder_id_fkey",
        "msgs_received",
        "stakeholders",
        ["stakeholder_id"],
        ["id"],
        ondelete="SET NULL",
    )

    pass


def downgrade() -> None:
    op.drop_column("msgs_received", "stakeholder_id")
    op.drop_constraint(
        "msgs_received_stakeholder_id_fkey", "msgs_received", type_="foreignkey"
    )
    op.drop_column("msgs_sent_users", "stakeholder_id")
    op.drop_constraint(
        "msgs_sent_users_stakeholder_id_fkey", "msgs_sent_users", type_="foreignkey"
    )
    pass
