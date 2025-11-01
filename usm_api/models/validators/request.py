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