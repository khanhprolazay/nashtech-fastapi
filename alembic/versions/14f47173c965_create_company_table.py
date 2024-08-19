"""create company table

Revision ID: 14f47173c965
Revises: 
Create Date: 2024-08-15 14:44:42.779449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas.company import CompanyMode
from uuid import uuid4
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '14f47173c965'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    company_table = op.create_table(
        "companies",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("mode", sa.Enum(CompanyMode), nullable=False, default=CompanyMode.PRIVATE),
        sa.Column("rating", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        
        sa.CheckConstraint("rating >= 0 AND rating <= 5", name="rating_check"),
    )

    op.create_index("ix_companies_name", "companies", ["name"])

    # Seed data
    op.bulk_insert( company_table, [{
        "id": "1161dbf0-132e-4f89-a121-c5e9ebba48ec",
        "name": "NashTech",
        "description": "This is NashTech",
        "mode": CompanyMode.PRIVATE,
        "rating": 5,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }])

    op.bulk_insert( company_table, [{
        "id": "0c5300ee-3b42-4e9e-8a4c-08626de7a889",
        "name": "Bosch",
        "description": "This is Bosch",
        "mode": CompanyMode.PRIVATE,
        "rating": 5,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }])


def downgrade() -> None:
    op.drop_table("companies")
    op.execute("DROP TYPE companymode;")
