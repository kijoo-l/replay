from __future__ import annotations

from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User, UserRole
from app.repositories.performance_repository import PerformanceRepository
from app.schemas.performance import (
    PerformanceCreate,
    PerformanceUpdate,
    PerformanceOut,
)

router = APIRouter(prefix="/performances", tags=["Performances"])


def _ensure_can_manage(user: User, club_id: Optional[int]) -> None:
    """
    공연 등록/수정/삭제 권한:
    - ADMIN
    - 또는 본인 소속 동아리 공연
    """
    if user.role == UserRole.ADMIN:
        return
    if club_id is not None and user.club_id == club_id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="공연을 관리할 권한이 없습니다.",
    )


@router.get("", response_model=List[PerformanceOut])
def list_performances(
    region: Optional[str] = Query(default=None),
    theme: Optional[str] = Query(default=None),
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
):
    return PerformanceRepository.list(
        db=db,
        region=region,
        theme=theme,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{performance_id}", response_model=PerformanceOut)
def get_performance(
    performance_id: int,
    db: Session = Depends(get_db),
):
    performance = PerformanceRepository.get(db, performance_id)
    if not performance:
        raise HTTPException(status_code=404, detail="공연 정보를 찾을 수 없습니다.")
    return performance


@router.post("", response_model=PerformanceOut, status_code=status.HTTP_201_CREATED)
def create_performance(
    data: PerformanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ensure_can_manage(current_user, data.club_id)
    return PerformanceRepository.create(db, data)


@router.patch("/{performance_id}", response_model=PerformanceOut)
def update_performance(
    performance_id: int,
    data: PerformanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    performance = PerformanceRepository.get(db, performance_id)
    if not performance:
        raise HTTPException(status_code=404, detail="공연 정보를 찾을 수 없습니다.")

    _ensure_can_manage(current_user, performance.club_id)
    return PerformanceRepository.update(db, performance, data)


@router.delete("/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_performance(
    performance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    performance = PerformanceRepository.get(db, performance_id)
    if not performance:
        raise HTTPException(status_code=404, detail="공연 정보를 찾을 수 없습니다.")

    _ensure_can_manage(current_user, performance.club_id)
    PerformanceRepository.delete(db, performance)
    return None
