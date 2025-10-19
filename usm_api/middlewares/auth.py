import jwt
from typing import List, Optional
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import PyJWTError
from sqlmodel import select
from models import db_models
from config import Config
from utility.database.sql_utils import engine
from fastapi.responses import JSONResponse
from models import validator_models
from sqlmodel import Session

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        algorithms: Optional[List[str]] = None,
        excluded_paths: Optional[List[str]] = None,
    ):
        super().__init__(app)
        self.secret_key = Config.SECRET_KEY
        self.engine = engine
        self.user_model = db_models.User
        self.algorithms = algorithms or ["HS256"]
        self.excluded_paths = excluded_paths or [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health",
            "/auth/login",
            "/auth/refresh",
        ]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip authentication for excluded paths
        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            error_response = validator_models.ErrorResponse(
                error="Invalid Authorization header",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response.model_dump(),
            )

        token = auth_header.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithms)
        except jwt.ExpiredSignatureError:
            error_response = validator_models.ErrorResponse(
                error="Token has expired",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response.model_dump(),
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            )
        except PyJWTError:
            error_response = validator_models.ErrorResponse(
                error="Invalid token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response.model_dump(),
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            )

        # Identify user id/email in token payload (simplejwt uses "user_id")
        user_identifier = None
        identifier_by = None
        if "user_id" in payload:
            user_identifier = payload["user_id"]
            identifier_by = "id"

        if user_identifier is None:
            error_response = validator_models.ErrorResponse(
                error="Token payload does not contain user identifier",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response.model_dump(),
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            )

        # Resolve user from DB using async session
        with Session(self.engine) as session:
            user = None
            # SQLModel supports get()
            try:
                user = session.get(self.user_model, int(user_identifier))
            except Exception:
                # fallback to select if get fails
                result = session.exec(
                    select(self.user_model).where(self.user_model.id == int(user_identifier))
                )
                user = result.scalar_one_or_none()

        if not user:
            error_response = validator_models.ErrorResponse(
                error="User not found",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response.model_dump(),
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            )

        if not getattr(user, "is_active", True):
            error_response = validator_models.ErrorResponse(
                error="User is inactive",
                status_code=status.HTTP_403_FORBIDDEN,
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=error_response.model_dump(),
            )

        # Attach SQLModel user to request.state
        request.state.user = user
        return await call_next(request)