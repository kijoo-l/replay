"""학교·동아리 및 관리자 매핑 테이블 추가

Revision ID: 75b17e3dc042
Revises:
Create Date: 2025-12-15 06:14:05.172931
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "75b17e3dc042"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # schools
    op.create_table(
        "schools",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=True),
        sa.Column("code", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_schools_name"), "schools", ["name"], unique=False)

    # clubs
    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("genre", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clubs_name"), "clubs", ["name"], unique=False)
    op.create_index(op.f("ix_clubs_school_id"), "clubs", ["school_id"], unique=False)

    # ---- 안전 정리: 예전 테스트 테이블(test_items) 제거 (있을 때만) ----
    # Postgres에서 index/table 없으면 터지므로 IF EXISTS로 처리
    op.execute("DROP INDEX IF EXISTS ix_test_items_id;")
    op.execute("DROP INDEX IF EXISTS ix_test_items_name;")
    op.execute("DROP TABLE IF EXISTS test_items CASCADE;")


def downgrade() -> None:
    # downgrade에서는 운영에서 거의 안 쓰지만, 최소한 안전하게 되돌림만 작성
    op.drop_index(op.f("ix_clubs_school_id"), table_name="clubs")
    op.drop_index(op.f("ix_clubs_name"), table_name="clubs")
    op.drop_table("clubs")

    op.drop_index(op.f("ix_schools_name"), table_name="schools")
    op.drop_table("schools")

    # test_items는 굳이 복구하지 않음 (운영/배포 기준 테이블 아님)
