"""Initial DB setup

Revision ID: initial_setup
Down revision ID: None

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = 'initial_setup'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'links',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('owner', sa.String(length=50), nullable=True),
        sa.Column('owner_id', sa.String(length=255), nullable=True),
        sa.Column('password', postgresql.BYTEA(), nullable=True),
        sa.Column('endpoint', sa.String(length=20), nullable=True),
        sa.Column('url', sa.String(length=300), nullable=True),
        sa.Column('switch_date', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'hash_salts',
        sa.Column('link_id', sa.Integer(), nullable=True),
        sa.Column('salt', postgresql.BYTEA(), nullable=True),
        sa.ForeignKeyConstraint(
            ['link_id'], ['links.id'],
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )


def downgrade():
    op.drop_table('hash_salts')
    op.drop_table('links')

    