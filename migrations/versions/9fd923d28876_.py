"""empty message

Revision ID: 9fd923d28876
Revises: 
Create Date: 2019-02-21 16:12:50.117588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fd923d28876'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('inn', sa.String(length=20), nullable=True),
    sa.Column('ogrn', sa.String(length=20), nullable=True),
    sa.Column('kpp', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization', sa.Integer(), nullable=True),
    sa.Column('number', sa.String(length=25), nullable=True),
    sa.Column('customer', sa.String(length=150), nullable=True),
    sa.Column('the_total_cost', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('template_fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('template', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('alias', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['template'], ['templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('orgnization', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('patronymic', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('performer', sa.Boolean(), nullable=True),
    sa.Column('appraiser', sa.Boolean(), nullable=True),
    sa.Column('signer', sa.Boolean(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('controler', sa.Boolean(), nullable=True),
    sa.Column('can_see_all_documents', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['orgnization'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('appraisers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.Integer(), nullable=True),
    sa.Column('employee', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['employee'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('controlers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.Integer(), nullable=True),
    sa.Column('employee', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['employee'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('performers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.Integer(), nullable=True),
    sa.Column('employee', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['employee'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('signers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.Integer(), nullable=True),
    sa.Column('employee', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['employee'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signers')
    op.drop_table('performers')
    op.drop_table('controlers')
    op.drop_table('appraisers')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('template_fields')
    op.drop_table('documents')
    op.drop_table('templates')
    op.drop_table('organizations')
    # ### end Alembic commands ###