"""create task table

Revision ID: 772c93627e22
Revises: 4cbfe7f38774
Create Date: 2024-08-15 14:45:02.062266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from schemas.task import TaskPriority, TaskStatus


# revision identifiers, used by Alembic.
revision: str = '772c93627e22'
down_revision: Union[str, None] = '4cbfe7f38774'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('summary', sa.String(), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.Enum(TaskStatus), nullable=False),
        sa.Column('priority', sa.Enum(TaskPriority), nullable=False, default=TaskPriority.LOW),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.UUID, sa.ForeignKey('users.id'), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('tasks')
    op.execute('DROP TYPE taskstatus')
    op.execute('DROP TYPE taskpriority')
