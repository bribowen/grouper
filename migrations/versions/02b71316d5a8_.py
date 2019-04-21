"""empty message

Revision ID: 02b71316d5a8
Revises: 
Create Date: 2019-04-17 08:58:56.948855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02b71316d5a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('uin', sa.Integer(), nullable=False),
    sa.Column('requester_fname', sa.String(length=60), nullable=True),
    sa.Column('requester_lname', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], ),
    sa.ForeignKeyConstraint(['uin'], ['profile.uin'], ),
    sa.PrimaryKeyConstraint('project_id', 'uin')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    # ### end Alembic commands ###