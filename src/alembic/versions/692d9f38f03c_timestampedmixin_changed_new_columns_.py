"""TimestampedMixin changed - new columns date_start, date_from

Revision ID: 692d9f38f03c
Revises: e0019a7c3018
Create Date: 2023-07-02 14:01:28.538715

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "692d9f38f03c"
down_revision = "e0019a7c3018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("comments", "created_at", new_column_name="date_from")
    op.add_column("comments", sa.Column("date_to", sa.DateTime(), nullable=True))
    op.alter_column("groups", "created_at", new_column_name="date_from")
    op.add_column("groups", sa.Column("date_to", sa.DateTime(), nullable=True))
    op.alter_column("groups_users", "created_at", new_column_name="date_from")
    op.add_column("groups_users", sa.Column("date_to", sa.DateTime(), nullable=True))
    op.alter_column("likes", "created_at", new_column_name="date_from")
    op.add_column("likes", sa.Column("date_to", sa.DateTime(), nullable=True))
    op.alter_column("posts", "created_at", new_column_name="date_from")
    op.add_column("posts", sa.Column("date_to", sa.DateTime(), nullable=True))
    op.alter_column("threat_categories", "created_at", new_column_name="date_from")
    op.add_column(
        "threat_categories",
        sa.Column("date_to", sa.DateTime(), nullable=True),
    )
    op.alter_column("users", "created_at", new_column_name="date_from")
    op.add_column("users", sa.Column("date_to", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.alter_column("users", "date_from", new_column_name="created_at")
    op.drop_column("users", "date_to")
    op.alter_column("threat_categories", "date_from", new_column_name="created_at")
    op.drop_column("threat_categories", "date_to")
    op.alter_column("posts", "date_from", new_column_name="created_at")
    op.drop_column("posts", "date_to")
    op.alter_column("likes", "date_from", new_column_name="created_at")
    op.drop_column("likes", "date_to")
    op.alter_column("groups_users", "date_from", new_column_name="created_at")
    op.drop_column("groups_users", "date_to")
    op.alter_column("groups", "date_from", new_column_name="created_at")
    op.drop_column("groups", "date_to")
    op.alter_column("comments", "date_from", new_column_name="created_at")
    op.drop_column("comments", "date_to")
