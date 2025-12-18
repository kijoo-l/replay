from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List
from app.models.performance import Performance
from app.schemas.performance import PerformanceCreate, PerformanceUpdate


class PerformanceRepository:

    @staticmethod
    def create(db: Session, data: PerformanceCreate) -> Performance:
        performance = Performance(**data.model_dump())
        db.add(performance)
        db.commit()
        db.refresh(performance)
        return performance

    @staticmethod
    def get(db: Session, performance_id: int) -> Optional[Performance]:
        return db.query(Performance).filter(Performance.id == performance_id).first()

    @staticmethod
    def list(
        db: Session,
        region: Optional[str],
        theme: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Performance]:
        q = db.query(Performance)
        if region:
            q = q.filter(Performance.region == region)
        if theme:
            q = q.filter(Performance.theme_category == theme)
        if start_date:
            q = q.filter(Performance.performance_date >= start_date)
        if end_date:
            q = q.filter(Performance.performance_date <= end_date)
        return q.order_by(Performance.performance_date).all()

    @staticmethod
    def list_by_club(db: Session, club_id: int) -> List[Performance]:
        return db.query(Performance).filter(Performance.club_id == club_id).all()

    @staticmethod
    def update(db: Session, performance: Performance, data: PerformanceUpdate):
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(performance, k, v)
        db.commit()
        db.refresh(performance)
        return performance

    @staticmethod
    def delete(db: Session, performance: Performance):
        db.delete(performance)
        db.commit()
