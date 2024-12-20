"""empty message

Revision ID: 2f0c1a6b9eb6
Revises: 45128c2b29a3
Create Date: 2024-04-29 21:40:32.065518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f0c1a6b9eb6'
down_revision = '45128c2b29a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('dni', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=9), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
