"""empty base

Revision ID: aea670db9918
Revises: 59c3410bcd3e
Create Date: 2025-11-21 16:08:42.452026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aea670db9918'
down_revision: Union[str, Sequence[str], None] = '59c3410bcd3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
