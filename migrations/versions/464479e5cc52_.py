"""empty message

Revision ID: 464479e5cc52
Revises: d01e31b25890
Create Date: 2020-08-17 12:07:26.506425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464479e5cc52'
down_revision = 'd01e31b25890'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('satisfaction')
    op.add_column('agent', sa.Column('date_uploaded', sa.DateTime(), nullable=False))
    op.drop_constraint(None, 'agent', type_='foreignkey')
    op.drop_column('agent', 'dob')
    op.drop_column('agent', 'date_employed')
    op.drop_column('agent', 'sacked')
    op.drop_column('agent', 'clientSatisfaction')
    op.drop_column('agent', 'ssn')
    op.add_column('apartment', sa.Column('agent', sa.Integer(), nullable=True))
    op.add_column('apartment', sa.Column('floor_plan_file', sa.String(length=20), nullable=False))
    op.add_column('apartment', sa.Column('floor_plan_photo_data', sa.LargeBinary(), nullable=True))
    op.alter_column('apartment', 'love',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'apartment', type_='foreignkey')
    op.create_foreign_key(None, 'apartment', 'agent', ['agent'], ['id'])
    op.drop_column('apartment', 'front_plan_photo_data')
    op.drop_column('apartment', 'clientSatisfaction')
    op.drop_column('apartment', 'front_plan_file')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('front_plan_file', sa.VARCHAR(length=20), nullable=False))
    op.add_column('apartment', sa.Column('clientSatisfaction', sa.INTEGER(), nullable=True))
    op.add_column('apartment', sa.Column('front_plan_photo_data', sa.BLOB(), nullable=True))
    op.drop_constraint(None, 'apartment', type_='foreignkey')
    op.create_foreign_key(None, 'apartment', 'satisfaction', ['clientSatisfaction'], ['id'])
    op.alter_column('apartment', 'love',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('apartment', 'floor_plan_photo_data')
    op.drop_column('apartment', 'floor_plan_file')
    op.drop_column('apartment', 'agent')
    op.add_column('agent', sa.Column('ssn', sa.INTEGER(), nullable=False))
    op.add_column('agent', sa.Column('clientSatisfaction', sa.INTEGER(), nullable=True))
    op.add_column('agent', sa.Column('sacked', sa.BOOLEAN(), nullable=True))
    op.add_column('agent', sa.Column('date_employed', sa.VARCHAR(), nullable=False))
    op.add_column('agent', sa.Column('dob', sa.VARCHAR(), nullable=False))
    op.create_foreign_key(None, 'agent', 'satisfaction', ['clientSatisfaction'], ['id'])
    op.drop_column('agent', 'date_uploaded')
    op.create_table('satisfaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=True),
    sa.Column('sales', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
