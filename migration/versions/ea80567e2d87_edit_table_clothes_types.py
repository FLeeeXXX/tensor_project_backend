"""EDIT TABLE clothes_types

Revision ID: ea80567e2d87
Revises: a1632665a139
Create Date: 2024-05-25 21:19:25.152307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea80567e2d87'
down_revision = 'a1632665a139'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clothes_types', sa.Column('clothes_type', sa.String(), nullable=False))
    op.drop_constraint('clothes_types_type_key', 'clothes_types', type_='unique')
    op.create_unique_constraint(None, 'clothes_types', ['clothes_type'])
    op.drop_column('clothes_types', 'type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clothes_types', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'clothes_types', type_='unique')
    op.create_unique_constraint('clothes_types_type_key', 'clothes_types', ['type'])
    op.drop_column('clothes_types', 'clothes_type')
    # ### end Alembic commands ###