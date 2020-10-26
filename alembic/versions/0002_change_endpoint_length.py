"""Change endpoint length

Revision ID: 0002
Down revision ID: 0001

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = '0002_change_endpoint_length'
down_revision = '0001_initial_setup'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('links', 'endpoint', type_=sa.String(100))


def downgrade():
    op.alter_column('links', 'endpoint', type_=sa.String(20))
