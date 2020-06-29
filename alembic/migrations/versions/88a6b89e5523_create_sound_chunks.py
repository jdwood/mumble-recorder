"""create sound chunks

Revision ID: 88a6b89e5523
Revises: 
Create Date: 2020-04-15 01:51:26.436500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88a6b89e5523'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE sound_chunks (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR,
            pcm_chunk BYTEA,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX ON sound_chunks (created_at);
        CREATE INDEX ON sound_chunks (created_at DESC);
    """)


def downgrade():
    op.execute("""
        DROP TABLE sound_chunks;
    """)
