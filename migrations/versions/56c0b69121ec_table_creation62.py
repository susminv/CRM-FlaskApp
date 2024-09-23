"""table creation62

Revision ID: 56c0b69121ec
Revises: 2a1947e02ce3
Create Date: 2024-09-23 12:04:44.530355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56c0b69121ec'
down_revision = '2a1947e02ce3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gender', sa.String(length=5), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('gender')

    # ### end Alembic commands ###
