"""empty message

Revision ID: c535f7ee76d1
Revises: fb2ae36bd248
Create Date: 2019-10-28 12:25:25.912597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c535f7ee76d1'
down_revision = '1d466ee887b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('gdoc_link', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resume', 'gdoc_link')
    # ### end Alembic commands ###
