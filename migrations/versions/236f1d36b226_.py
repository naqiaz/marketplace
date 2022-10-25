"""empty message

Revision ID: 236f1d36b226
Revises: 669aaa853b69
Create Date: 2020-07-16 17:12:07.218204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '236f1d36b226'
down_revision = '669aaa853b69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('type', sa.String(length=64), nullable=False))
    op.add_column('user', sa.Column('type', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'type')
    op.drop_column('company', 'type')
    # ### end Alembic commands ###
