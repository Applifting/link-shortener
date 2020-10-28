"""Change endpoint length

Revision ID: change_endpoint_length
Down revision ID: initial_setup

"""
import sqlalchemy as sa
from alembic import op


revision = 'change_endpoint_length'
down_revision = 'initial_setup'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('links', 'endpoint', type_=sa.String(100))


def downgrade():
    op.alter_column('links', 'endpoint', type_=sa.String(20))
