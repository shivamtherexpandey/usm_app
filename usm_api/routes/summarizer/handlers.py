from fastapi.responses import Response, JSONResponse
from fastapi import status
from fastapi.requests import Request
from fastapi import APIRouter
from models import validator_models, db_models
from utility import logger
from utility import Helper
from async_tasks import generate_summary

router = APIRouter(tags=['summarizer'])

@router.post('/summarize')
def summarize(request: Request, request_body: validator_models.SummarizerRequest):
    if not request.state.user:
        logger.error("Unauthorized access attempt to /summarize")
        error_response = validator_models.ErrorResponse(
            error="User is not authenticated",
            status_code=status.HTTP_403_FORBIDDEN,
        )
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response.model_dump(),
        )
    
    if not Helper.is_webpage(request_body.url):
        logger.error("Invalid URL provided for summarization")
        error_response = validator_models.ErrorResponse(
            error="Invalid URL provided for summarization",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump(),
        )

    # Make Summarization Object
    user_id = request.state.user.id
    with request.state.db() as session:
        id = session.query(db_models.Summary).filter(
                db_models.Summary.url == request_body.url,
                db_models.Summary.user_id == user_id,
                db_models.Summary.is_deleted == False,
                db_models.Summary.processed == True
            ).first()

        if id:
            logger.error(f"Summarization request for existing URL by user {user_id}")
            error_response = validator_models.ErrorResponse(
                error="Summarization for this URL already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=error_response.model_dump(),
            )
           
        summarization = db_models.Summary(
            url=request_body.url,
            user_id=user_id,
            processed=False
        )
        session.add(summarization)
        session.commit()
        session.refresh(summarization)
        logger.info(f"Created summarization request with id {summarization.id} for user id {user_id}")

    # Make URL Summarization Request
    generate_summary.apply_async(args=[summarization.id])

    # Return Generic Response
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"msg": "summarization in progress", "id": summarization.id},
    )