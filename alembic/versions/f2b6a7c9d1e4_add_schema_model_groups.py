"""add schema model groups

Revision ID: f2b6a7c9d1e4
Revises: e4b7c2d1a9f0
Create Date: 2026-06-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f2b6a7c9d1e4'
down_revision: Union[str, Sequence[str], None] = 'e4b7c2d1a9f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'schema_model_groups',
        sa.Column('group_id', sa.String(length=64), nullable=False, comment='目录ID'),
        sa.Column('project_id', sa.Integer(), nullable=False, comment='所属项目ID'),
        sa.Column('branch_id', sa.String(length=64), nullable=True, comment='所属分支ID'),
        sa.Column('parent_id', sa.String(length=64), nullable=True, comment='父目录ID'),
        sa.Column('name', sa.String(length=128), nullable=False, comment='目录名称'),
        sa.Column('create_by', sa.String(length=64), nullable=True),
        sa.Column(
            'create_time',
            postgresql.TIMESTAMP(precision=0),
            server_default=sa.text('now()'),
            nullable=True,
            comment='创建时间',
        ),
        sa.Column('update_by', sa.String(length=64), nullable=True),
        sa.Column(
            'update_time',
            postgresql.TIMESTAMP(precision=0),
            server_default=sa.text('now()'),
            nullable=True,
            comment='更新时间',
        ),
        sa.Column('remark', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sort_no', sa.Float(), nullable=True, server_default='0', comment='排序号'),
        sa.Column('del_flag', sa.String(length=1), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('group_id'),
        comment='JSON Schema 数据模型目录表',
    )
    op.create_index('ix_schema_model_groups_project_id', 'schema_model_groups', ['project_id'], unique=False)
    op.create_index('ix_schema_model_groups_parent_id', 'schema_model_groups', ['parent_id'], unique=False)
    op.create_index('ix_schema_model_groups_branch_id', 'schema_model_groups', ['branch_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_schema_model_groups_branch_id', table_name='schema_model_groups')
    op.drop_index('ix_schema_model_groups_parent_id', table_name='schema_model_groups')
    op.drop_index('ix_schema_model_groups_project_id', table_name='schema_model_groups')
    op.drop_table('schema_model_groups')
