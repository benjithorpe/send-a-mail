"""empty message

Revision ID: c71e5193e432
Revises: 
Create Date: 2022-01-18 22:32:54.811676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c71e5193e432'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('student', 'email',
               existing_type=sa.VARCHAR(length=75),
               nullable=True)
    op.alter_column('student', 'profile_picture',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('student', 'profile_picture',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('student', 'email',
               existing_type=sa.VARCHAR(length=75),
               nullable=False)
    # ### end Alembic commands ###
