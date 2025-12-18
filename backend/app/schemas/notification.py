from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: int
    recipient_user_id: int
    type: str
    entity_id: Optional[int] = None
    payload: Optional[str] = None
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
