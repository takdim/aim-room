"""add_token_to_room_bookings

Revision ID: be75122018ed
Revises: b3f8a2c1d9e0
Create Date: 2026-07-09 14:31:05.159869

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'be75122018ed'
down_revision = 'b3f8a2c1d9e0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('room_bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=32), nullable=True))
        batch_op.create_unique_constraint(None, ['token'])

    # Backfill token for existing rows
    bookings = table('room_bookings', column('id', sa.Integer), column('token', sa.String))
    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id FROM room_bookings WHERE token IS NULL")).fetchall()
    for row in rows:
        conn.execute(
            sa.text("UPDATE room_bookings SET token = :token WHERE id = :id"),
            {"token": uuid.uuid4().hex, "id": row[0]},
        )


def downgrade():
    with op.batch_alter_table('room_bookings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('token')
