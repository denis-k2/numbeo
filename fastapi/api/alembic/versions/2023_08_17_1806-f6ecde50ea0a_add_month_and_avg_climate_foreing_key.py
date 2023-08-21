"""add month and avg_climate foreing key

Revision ID: f6ecde50ea0a
Revises: 
Create Date: 2023-08-17 18:06:26.961467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6ecde50ea0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    month = op.create_table(
        'month_aux',
        sa.Column('month_id', sa.SmallInteger(), nullable=False),
        sa.Column('month_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('month_id', name='pk_month')
    )
    op.bulk_insert(
        month,
        [
            {"month_id": 1, "month_name": "january"},
            {"month_id": 2, "month_name": "february"},
            {"month_id": 3, "month_name": "march"},
            {"month_id": 4, "month_name": "april"},
            {"month_id": 5, "month_name": "may"},
            {"month_id": 6, "month_name": "june"},
            {"month_id": 7, "month_name": "july"},
            {"month_id": 8, "month_name": "august"},
            {"month_id": 9, "month_name": "september"},
            {"month_id": 10, "month_name": "october"},
            {"month_id": 11, "month_name": "november"},
            {"month_id": 12, "month_name": "december"}
        ],
    )
    op.create_foreign_key(
        "fk_month",
        "avg_climate",
        "month_aux",
        ["month"],
        ["month_id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("fk_month"), "avg_climate", type_="foreignkey")
    op.drop_table('month_aux')
    # ### end Alembic commands ###
