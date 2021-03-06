"""empty message

Revision ID: a9b894b5ff2a
Revises: 0b2b402c19c7
Create Date: 2020-07-25 20:31:06.669684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9b894b5ff2a'
down_revision = '0b2b402c19c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('messages_chat_user1_chat_user2_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'chats', ['chat_user1', 'chat_user2'], ['user1_id', 'user2_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_chat_user1_chat_user2_fkey', 'messages', 'chats', ['chat_user1', 'chat_user2'], ['user1_id', 'user2_id'])
    # ### end Alembic commands ###
