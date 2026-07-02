"""add class_schedule_lecturers many-to-many and class_name field

Revision ID: b3f8a2c1d9e0
Revises: 2552279dd0a0
Create Date: 2026-07-01

"""
from alembic import op
import sqlalchemy as sa

revision = 'b3f8a2c1d9e0'
down_revision = '2552279dd0a0'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Buat tabel junction many-to-many
    op.create_table(
        'class_schedule_lecturers',
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('lecturer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], name='fk_csl_lecturer_id'),
        sa.ForeignKeyConstraint(['schedule_id'], ['class_schedules.id'], name='fk_csl_schedule_id'),
        sa.PrimaryKeyConstraint('schedule_id', 'lecturer_id'),
    )

    # 2. Migrasi data lama: salin lecturer_id yang ada ke junction table
    op.execute(
        "INSERT INTO class_schedule_lecturers (schedule_id, lecturer_id) "
        "SELECT id, lecturer_id FROM class_schedules WHERE lecturer_id IS NOT NULL"
    )

    # 3. Tambah class_name dan hapus lecturer_id
    #    Di MySQL harus drop FK constraint dulu sebelum drop column
    with op.batch_alter_table('class_schedules', schema=None) as batch_op:
        batch_op.add_column(sa.Column('class_name', sa.String(150), nullable=True))
        batch_op.drop_constraint('class_schedules_ibfk_3', type_='foreignkey')
        batch_op.drop_column('lecturer_id')


def downgrade():
    with op.batch_alter_table('class_schedules', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lecturer_id', sa.Integer(), nullable=True))
        batch_op.drop_column('class_name')

    # Kembalikan data lecturer_id dari junction table (ambil satu per jadwal)
    op.execute(
        "UPDATE class_schedules SET lecturer_id = ("
        "  SELECT lecturer_id FROM class_schedule_lecturers"
        "  WHERE schedule_id = class_schedules.id LIMIT 1"
        ")"
    )

    op.drop_table('class_schedule_lecturers')
