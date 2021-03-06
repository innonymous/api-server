"""empty message

Revision ID: a7d2887aa71f
Revises: 
Create Date: 2021-08-24 13:08:21.804798+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a7d2887aa71f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rooms',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('users',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('active', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('messages',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('type', sa.Enum('text', name='messagetype'), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('room_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['room_uuid'], ['rooms.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('users')
    op.drop_table('rooms')
    # ### end Alembic commands ###
