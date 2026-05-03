"""create user table

Revision ID: 84e8b877b468
Revises: b44aee0fecba
Create Date: 2026-05-02 21:27:32.583482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84e8b877b468'
down_revision: Union[str, Sequence[str], None] = 'b44aee0fecba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user", sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("email", sa.String(), nullable=False),
    sa.Column("password", sa.String(), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("email"))
    
    pass


def downgrade() -> None:
    op.drop_table("user")
    pass
