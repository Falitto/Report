"""empty message

Revision ID: 5214912ddf1b
Revises: 93921db83d67
Create Date: 2019-02-28 18:38:19.104473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5214912ddf1b'
down_revision = '93921db83d67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('templates', sa.Column('file_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('templates', 'file_name')
    # ### end Alembic commands ###
