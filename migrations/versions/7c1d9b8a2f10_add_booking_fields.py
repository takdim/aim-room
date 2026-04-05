"""add booking fields

Revision ID: 7c1d9b8a2f10
Revises: 9f3b2c1d8a72
Create Date: 2026-04-05 15:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "7c1d9b8a2f10"
down_revision = "9f3b2c1d8a72"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("room_bookings", sa.Column("borrower_name", sa.String(length=120), nullable=True))
    op.add_column("room_bookings", sa.Column("phone_number", sa.String(length=40), nullable=True))
    op.add_column("room_bookings", sa.Column("borrower_email", sa.String(length=120), nullable=True))
    op.add_column("room_bookings", sa.Column("organization", sa.String(length=150), nullable=True))
    op.add_column("room_bookings", sa.Column("notes", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("room_bookings", "notes")
    op.drop_column("room_bookings", "organization")
    op.drop_column("room_bookings", "borrower_email")
    op.drop_column("room_bookings", "phone_number")
    op.drop_column("room_bookings", "borrower_name")
