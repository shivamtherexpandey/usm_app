from fastapi import Request, HTTPException
from models import validator_models
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=validator_models.ErrorResponse(error=str(exc.detail), status_code=exc.status_code).model_dump(),
    )

def register_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
