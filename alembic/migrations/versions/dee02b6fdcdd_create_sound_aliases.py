"""create sound_aliases

Revision ID: dee02b6fdcdd
Revises: 88a6b89e5523
Create Date: 2020-06-30 01:19:29.072672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dee02b6fdcdd'
down_revision = '88a6b89e5523'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE sound_aliases (
            id BIGSERIAL PRIMARY KEY,
            sound_chunk BYTEA,
            name VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX ON sound_aliases (name);
    """)


def downgrade():
    op.execute("""
        DROP TABLE sound_aliases;
    """)
