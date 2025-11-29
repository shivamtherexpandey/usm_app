from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from sqlalchemy.orm import Session
from utility import database_helper


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.session_maker = database_helper.SessionLocal

    async def dispatch(self, request: Request, call_next):
        # Create a new session and attach to request.state
        request.state.db = self.session_maker
        try:
            response = await call_next(request)
            return response
        except Exception:
            # On exception, rollback the transaction to avoid partial state
            try:
                request.state.db.rollback()
            except Exception:
                pass
            raise
        finally:
            # Close the session
            try:
                request.state.db.close()
            except Exception:
                pass
