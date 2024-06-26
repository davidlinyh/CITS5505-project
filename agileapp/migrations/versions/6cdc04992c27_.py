"""empty message

Revision ID: 6cdc04992c27
Revises: 6b1d855ddd96
Create Date: 2024-05-10 02:53:50.051115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cdc04992c27'
down_revision = '6b1d855ddd96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lost_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lost_item', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
