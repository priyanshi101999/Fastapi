"""Add title column into posts table

Revision ID: b44aee0fecba
Revises: 076e69104fbb
Create Date: 2026-05-02 21:10:21.447699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b44aee0fecba'
down_revision: Union[str, Sequence[str], None] = '076e69104fbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("post", column_name="title")
    pass
