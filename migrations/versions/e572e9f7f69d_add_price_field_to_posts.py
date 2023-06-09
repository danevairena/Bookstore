"""add price field to posts

Revision ID: e572e9f7f69d
Revises: 654f89b6d9c0
Create Date: 2023-06-02 13:27:44.531537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e572e9f7f69d'
down_revision = '654f89b6d9c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###
