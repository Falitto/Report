"""empty message

Revision ID: 7f38fe81c828
Revises: cfd40bed00b5
Create Date: 2019-02-28 10:26:38.843693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f38fe81c828'
down_revision = 'cfd40bed00b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('template_fields', sa.Column('index', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('template_fields', 'index')
    # ### end Alembic commands ###