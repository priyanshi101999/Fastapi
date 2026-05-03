"""empty message

Revision ID: 076e69104fbb
Revises: 
Create Date: 2026-05-02 20:59:42.064134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '076e69104fbb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("post", sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                   sa.Column("content", sa.String(), nullable=False))
 
    pass


def downgrade() -> None:
    op.drop_table("post")
    pass
