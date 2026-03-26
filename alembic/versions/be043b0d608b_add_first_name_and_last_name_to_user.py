"""Add first_name and last_name to user

Revision ID: be043b0d608b
Revises: 87c6db12f85e
Create Date: 2026-03-26 15:48:21.502195
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'be043b0d608b'
down_revision: Union[str, Sequence[str], None] = '87c6db12f85e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add first_name and last_name columns to user table
    op.add_column('user', sa.Column('first_name', sa.String(length=255), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(length=255), nullable=False))


    op.execute("UPDATE \"user\" SET first_name = 'Unknown', last_name = 'Unknown' WHERE first_name IS NULL OR last_name IS NULL;")

    op.alter_column('user', 'first_name', nullable=False)
    op.alter_column('user', 'last_name', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove first_name and last_name columns
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')