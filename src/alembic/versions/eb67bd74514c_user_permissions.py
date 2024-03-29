"""User permissions

Revision ID: eb67bd74514c
Revises: be3282935a80
Create Date: 2023-06-23 11:01:27.517743

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "eb67bd74514c"
down_revision = "be3282935a80"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("permissions", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "permissions")
    # ### end Alembic commands ###
