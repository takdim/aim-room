"""add building name

Revision ID: 4b2a9b3d7f1c
Revises: cd64bb8ec645
Create Date: 2026-04-05 15:08:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "4b2a9b3d7f1c"
down_revision = "cd64bb8ec645"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("buildings", sa.Column("building_name", sa.String(length=120), nullable=True))


def downgrade():
    op.drop_column("buildings", "building_name")
