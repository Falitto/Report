"""empty message

Revision ID: 98c787683593
Revises: 8adafb33d10b
Create Date: 2019-03-20 09:24:16.699311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98c787683593'
down_revision = '8adafb33d10b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('field_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('document_fields', sa.Column('field_type', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'document_fields', 'field_types', ['field_type'], ['id'])
    op.add_column('template_fields', sa.Column('field_type', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'template_fields', 'field_types', ['field_type'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'template_fields', type_='foreignkey')
    op.drop_column('template_fields', 'field_type')
    op.drop_constraint(None, 'document_fields', type_='foreignkey')
    op.drop_column('document_fields', 'field_type')
    op.drop_table('field_types')
    # ### end Alembic commands ###