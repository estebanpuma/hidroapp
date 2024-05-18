"""empty message

Revision ID: 70134ddcacd5
Revises: b641aada8665
Create Date: 2024-05-17 22:09:58.695517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70134ddcacd5'
down_revision = 'b641aada8665'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('month',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pma_activity_month',
    sa.Column('month_id', sa.Integer(), nullable=False),
    sa.Column('pma_activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pma_activity_id'], ['pma_activity.id'], ),
    sa.PrimaryKeyConstraint('month_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pma_activity_month')
    op.drop_table('month')
    # ### end Alembic commands ###
