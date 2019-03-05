"""empty message

Revision ID: 1648e92146ec
Revises: 4117267dce97
Create Date: 2019-03-04 14:46:12.211681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1648e92146ec'
down_revision = '4117267dce97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('docs', sa.Column('result', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('docs', 'result')
    # ### end Alembic commands ###