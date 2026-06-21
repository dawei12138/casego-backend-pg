"""add schema model branch id

Revision ID: e4b7c2d1a9f0
Revises: c5a30dfe05b6
Create Date: 2026-06-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4b7c2d1a9f0'
down_revision: Union[str, Sequence[str], None] = 'c5a30dfe05b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'schema_models',
        sa.Column('branch_id', sa.String(length=64), nullable=True, comment='所属分支ID'),
    )
    op.create_index('ix_schema_models_branch_id', 'schema_models', ['branch_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_schema_models_branch_id', table_name='schema_models')
    op.drop_column('schema_models', 'branch_id')
