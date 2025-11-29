from pydantic import BaseModel, field_validator
from urllib.parse import urlparse


class SummarizerRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("url must be a non-empty string")
        v = v.strip()
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("url must be a valid HTTP or HTTPS URL")
        return v


class Pagination(BaseModel):
    page: int = 1
    offset: int = 10

    @field_validator("offset")
    def validate_offset(cls, v: int) -> int:
        if 1 <= v <= 100:
            return v
        raise ValueError("offset needs to be between 1 and 100")

    @field_validator("page")
    def validate_page(cls, v: int) -> int:
        if 1 <= v:
            return v
        raise ValueError("page needs to be more than 0")
