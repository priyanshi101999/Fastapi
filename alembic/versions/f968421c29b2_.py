"""empty message

Revision ID: f968421c29b2
Revises: eec8c295f881
Create Date: 2026-05-02 22:09:35.294992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f968421c29b2'
down_revision: Union[str, Sequence[str], None] = 'eec8c295f881'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("is_published", sa.Boolean(), nullable=False, server_default="TRUE")),
    op.add_column("post", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("post", "is_published")
    op.drop_column("post", "created_at")
    pass
