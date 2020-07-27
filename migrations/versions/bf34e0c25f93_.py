"""empty message

Revision ID: bf34e0c25f93
Revises: 1c880abbd229
Create Date: 2020-07-27 18:39:45.789603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf34e0c25f93'
down_revision = '1c880abbd229'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher_features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers_goal',
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('goals_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goals_id'], ['goals.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teachers_goal')
    op.drop_table('teacher_features')
    # ### end Alembic commands ###