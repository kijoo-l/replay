from sqlalchemy.orm import Session

from app.models.school import School
from app.models.club import Club
from app.utils.pagination import (
    paginate_query,
    apply_keyword_filter,
    apply_sort,
)


class SchoolRepository:
    """
    School / Club 목록 조회 전용 Repository
    공통 페이징·검색·정렬 유틸 적용
    """

    @staticmethod
    def list_schools(
        db: Session,
        page: int,
        size: int,
        keyword: str | None,
        sort: str | None,
    ):
        query = db.query(School)

        # 검색 (학교명 / 지역 / 코드)
        query = apply_keyword_filter(
            query,
            keyword,
            [School.name, School.region, School.code],
        )

        # 정렬
        query = apply_sort(query, sort, School)

        # 페이징
        return paginate_query(query, page, size)

    @staticmethod
    def list_clubs_by_school(
        db: Session,
        school_id: int,
        page: int,
        size: int,
        keyword: str | None,
        sort: str | None,
    ):
        query = (
            db.query(Club)
            .filter(Club.school_id == school_id)
        )

        # 검색 (동아리명 / 설명 / 장르)
        query = apply_keyword_filter(
            query,
            keyword,
            [Club.name, Club.description, Club.genre],
        )

        # 정렬
        query = apply_sort(query, sort, Club)

        # 페이징
        return paginate_query(query, page, size)
