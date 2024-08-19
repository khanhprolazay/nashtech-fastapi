"""create user table

Revision ID: 4cbfe7f38774
Revises: 14f47173c965
Create Date: 2024-08-15 14:44:57.311315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import datetime
from services.user import hash_password
from environment import DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision: str = '4cbfe7f38774'
down_revision: Union[str, None] = '14f47173c965'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column("is_admin", sa.Boolean, nullable=False, default=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("company_id", sa.UUID, sa.ForeignKey("companies.id"), nullable=True),
    )

    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_frt_las_name", "users", ["first_name", "last_name"])

    # Seed data
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "hashed_password": hash_password(DEFAULT_PASSWORD),
            "email": "john.doe@gmail.com",
            "is_active": True,
            "is_admin": True,
            "company_id": "1161dbf0-132e-4f89-a121-c5e9ebba48ec",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    ])

    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "janedoe",
            "hashed_password": hash_password(DEFAULT_PASSWORD),
            "email": "jahn.doe@gmail.com",
            "is_active": True,
            "is_admin": True,
            "company_id": "0c5300ee-3b42-4e9e-8a4c-08626de7a889",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    ])    

def downgrade() -> None:
    op.drop_table("users")
