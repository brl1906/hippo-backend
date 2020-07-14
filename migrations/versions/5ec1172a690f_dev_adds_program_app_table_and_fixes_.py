"""DEV adds program_app table and fixes hawaiian spelling in race table

Revision ID: 5ec1172a690f
Revises: f57f02a95449
Create Date: 2020-07-14 11:29:10.479937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ec1172a690f'
down_revision = 'f57f02a95449'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program_app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('is_interested', sa.Boolean(), nullable=True),
    sa.Column('date_approved', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('race', sa.Column('hawaiian', sa.Boolean(), nullable=True))
    op.drop_column('race', 'hawaiin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('race', sa.Column('hawaiin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('race', 'hawaiian')
    op.drop_table('program_app')
    # ### end Alembic commands ###
