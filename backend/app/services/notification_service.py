from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.models.notification import NotificationType
from app.repositories.notification_repository import NotificationRepository
from app.utils.websocket_manager import WebSocketManager
from app.schemas.notification import NotificationOut

# 전역 WebSocket 매니저 (echo와 공유)
ws_manager = WebSocketManager()


class NotificationService:
    @staticmethod
    async def notify_user(
        db: Session,
        user_id: int,
        type: NotificationType,
        message: str,
        entity_id: Optional[int] = None,
        payload: Optional[str] = None,
    ):
        # 1) DB 저장
        n = NotificationRepository.create(
            db=db,
            recipient_user_id=user_id,
            type=type,
            message=message,
            entity_id=entity_id,
            payload=payload,
        )

        # 2) WebSocket 실시간 푸시 (broadcast)
        await ws_manager.broadcast_json(
            {
                "type": "NOTIFICATION",
                "data": NotificationOut.model_validate(n).model_dump(),
            }
        )

        return n
