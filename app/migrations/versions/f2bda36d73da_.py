"""empty message

Revision ID: f2bda36d73da
Revises: 0ae5d08ccf9f
Create Date: 2020-03-28 15:12:47.076335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2bda36d73da'
down_revision = '0ae5d08ccf9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    op.drop_index('ix_post_timestamp', table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_post_timestamp', 'post', ['timestamp'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('about_me', sa.VARCHAR(length=140), nullable=True),
    sa.Column('last_seen', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    op.create_table('followers',
    sa.Column('follower_id', sa.INTEGER(), nullable=True),
    sa.Column('followed_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###
