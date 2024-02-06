"""Add chat_id

Revision ID: ae33f4132b93
Revises: b2326e6449f9
Create Date: 2024-02-05 18:14:17.258743

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'ae33f4132b93'
down_revision = 'b2326e6449f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('chat_id', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'chat_id')
    # ### end Alembic commands ###