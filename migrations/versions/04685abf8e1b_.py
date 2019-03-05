"""empty message

Revision ID: 04685abf8e1b
Revises: c535433f1203
Create Date: 2019-02-28 10:38:06.490360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04685abf8e1b'
down_revision = 'c535433f1203'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('alias', sa.String(length=255), nullable=True),
    sa.Column('template_field', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['template_field'], ['template_fields.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_fields')
    # ### end Alembic commands ###