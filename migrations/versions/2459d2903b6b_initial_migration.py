"""initial migration

Revision ID: 2459d2903b6b
Revises: None
Create Date: 2016-09-24 16:22:07.348055

"""

# revision identifiers, used by Alembic.
revision = '2459d2903b6b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passwords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passwords_title'), 'passwords', ['title'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_passwords_title'), table_name='passwords')
    op.drop_table('passwords')
    ### end Alembic commands ###
