"""Nombre Migracion

Revision ID: 975f5117a278
Revises: b86a05f98b60
Create Date: 2023-09-27 15:25:46.036673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '975f5117a278'
down_revision: Union[str, None] = 'b86a05f98b60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
