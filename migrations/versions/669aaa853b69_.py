"""empty message

Revision ID: 669aaa853b69
Revises: 
Create Date: 2020-07-09 17:13:33.855868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '669aaa853b69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotion', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_promotion_timestamp'), 'promotion', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_promotion_timestamp'), table_name='promotion')
    op.drop_column('promotion', 'timestamp')
    # ### end Alembic commands ###