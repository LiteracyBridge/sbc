"""add timestamps to msgs_sent_users and msgs_received

Revision ID: 51fe390d1f8d
Revises: 1b385a62dc57
Create Date: 2023-07-20 23:40:55.152766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "51fe390d1f8d"
down_revision = "1b385a62dc57"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Stakeholders
    op.add_column(
        "stakeholders",
        sa.Column("whatsapp_last_received", sa.DateTime(timezone=True), nullable=True),
    )

    # msgs_sent_users
    op.add_column(
        "msgs_sent_users",
        sa.Column(
            "message_sid",
            sa.Text(),
            nullable=True,
        ),
    )
    op.add_column(
        "msgs_sent_users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "msgs_sent_users",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )

    # msgs_received
    op.add_column(
        "msgs_received",
        sa.Column(
            "message_sid",
            sa.Text(),
            nullable=True,
        ),
    )
    op.add_column(
        "msgs_received",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "msgs_received",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )

    op.add_column(
        "msgs_sent",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "msgs_sent",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            default=sa.func.now(),
        ),
    )
    op.add_column(
        "msgs_sent",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("stakeholders", "whatsapp_last_received")

    op.drop_column("msgs_sent_users", "created_at")
    op.drop_column("msgs_sent_users", "updated_at")
    op.drop_column("msgs_sent_users", "message_sid")

    op.drop_column("msgs_received", "created_at")
    op.drop_column("msgs_received", "updated_at")
    op.drop_column("msgs_received", "message_sid")

    op.drop_column("msgs_sent", "created_at")
    op.drop_column("msgs_sent", "updated_at")
