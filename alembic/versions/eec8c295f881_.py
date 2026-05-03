"""empty message

Revision ID: eec8c295f881
Revises: 84e8b877b468
Create Date: 2026-05-02 21:44:39.515838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eec8c295f881'
down_revision: Union[str, Sequence[str], None] = '84e8b877b468'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_user_fk", source_table="post", referent_table="user", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_foreign_key("post_user_fk", table_name="post")
    op.drop_column("post", column_name="owner_id")
    pass
