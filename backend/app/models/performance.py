from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey
)
from app.database import Base


class Performance(Base):
    __tablename__ = "performances"

    id = Column(Integer, primary_key=True, index=True)

    # 소속
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    region = Column(String(100), nullable=False, index=True)
    theme_category = Column(String(100), nullable=False, index=True)

    poster_image_url = Column(String(500), nullable=True)

    performance_date = Column(Date, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
