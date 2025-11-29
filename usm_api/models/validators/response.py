from datetime import datetime
from sqlmodel import SQLModel
from models import db_models
from pydantic import BaseModel, field_validator


class SummaryResponse(BaseModel):
    id: int
    url: str
    summary: str | None
    processed: int | None
    created_at: datetime | str
    updated_at: datetime | str

    class Config:
        from_attributes = True

    @field_validator("created_at")
    def validate_created_at(v: datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @field_validator("updated_at")
    def validate_updated_at(v: datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")


class GetSummariesResponse(BaseModel):
    page: int
    offset: int
    summaries: list[SummaryResponse]
    user_id: int
