"""empty message

Revision ID: 3dcc5dc7d034
Revises: 8fcc403e21e8
Create Date: 2019-03-20 10:35:07.923790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dcc5dc7d034'
down_revision = '8fcc403e21e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subdivisions', sa.Column('organization', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'subdivisions', 'organizations', ['organization'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subdivisions', type_='foreignkey')
    op.drop_column('subdivisions', 'organization')
    # ### end Alembic commands ###