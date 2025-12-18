from __future__ import annotations

from math import ceil
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.schemas.common import ok, PageData, PaginationMeta
from app.schemas.notification import NotificationOut

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
def list_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    is_read: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = NotificationRepository.list_for_user(
        db=db,
        user_id=current_user.id,
        is_read=is_read,
        page=page,
        size=size,
    )

    total_pages = ceil(total / size) if size else 0
    meta = PaginationMeta(
        page=page,
        size=size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )
    data = PageData[NotificationOut](
        items=[NotificationOut.model_validate(i) for i in items],
        meta=meta,
    )
    return ok(data)


@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    n = NotificationRepository.get_by_id(db, notification_id)
    if not n:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")

    if n.recipient_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 알림만 처리할 수 있습니다.",
        )

    n = NotificationRepository.mark_read(db, n)
    return ok(NotificationOut.model_validate(n))
