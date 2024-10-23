"""Initial migration

Revision ID: 278a19ab5d62
Revises: 
Create Date: 2024-10-22 18:00:39.643532

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "278a19ab5d62"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "films",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("production_year", sa.Integer(), nullable=False),
        sa.Column(
            "production_country",
            sa.Enum("USA", "UK", "CANADA", "FRANCE", name="countryenum"),
            nullable=False,
        ),
        sa.Column(
            "genre",
            sa.Enum(
                "ACTION",
                "DRAMA",
                "COMEDY",
                "HORROR",
                "SCIENCE_FICTION",
                name="genreenum",
            ),
            nullable=False,
        ),
        sa.Column(
            "producer",
            sa.Enum(
                "LEGENDARY_PICTURES",
                "WARNER_BROS",
                "UNIVERSAL",
                "PIXAR",
                "DISNEY",
                "FRANK_DARABONT",
                name="producerenum",
            ),
            nullable=False,
        ),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("revenue", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("cover_image", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_films_id"), "films", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("USER", "ADMIN", name="roleenum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_films_id"), table_name="films")
    op.drop_table("films")
    # ### end Alembic commands ###
