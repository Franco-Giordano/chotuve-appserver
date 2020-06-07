"""empty message

Revision ID: 3d8e58d7d5cb
Revises: 98fd260fab21
Create Date: 2020-06-05 05:24:53.327229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d8e58d7d5cb'
down_revision = '98fd260fab21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('thumbnail_url', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'thumbnail_url')
    # ### end Alembic commands ###