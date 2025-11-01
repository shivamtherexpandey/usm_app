from pytz import timezone
from config import Config
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text, Boolean, DateTime, func
from models.db.user import User

_TZ = timezone(Config.TIMEZONE)

class Summary(SQLModel, table=True):
    __tablename__ = "summaries"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(..., max_length=2048, index=True)
    user_id: int = Field(..., foreign_key="usm_user_user.id", index=True)
    summary: Optional[str] = Field(default=None, sa_column=Column(Text))
    processed: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    is_deleted: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(_TZ),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(_TZ),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            server_onupdate=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))

Summary.user = Relationship(back_populates="summaries")