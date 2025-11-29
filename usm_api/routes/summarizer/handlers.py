from fastapi.responses import Response, JSONResponse
from fastapi import status
from fastapi.requests import Request
from fastapi import APIRouter, Depends
from models import validator_models, db_models
from utility import logger
from utility import Helper
from async_tasks import generate_summary
from datetime import datetime

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
    generate_summary.apply_async(args=[summarization.id], queue='summarization_queue')

    # Return Generic Response
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"msg": "Summarization in progress", "id": summarization.id},
    )

@router.get('/list')
def get_summary(request: Request, pagination: validator_models.Pagination= Depends()):
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

    user_id = request.state.user.id
    page = pagination.page
    offset = pagination.offset

    try:
        with request.state.db() as session:
            extracted_summary = session.query(db_models.Summary).filter(db_models.Summary.user_id == user_id, db_models.Summary.is_deleted == False).order_by(-db_models.Summary.updated_at).offset((page-1)*offset).limit(offset).all()
            
            extracted_summary = list(extracted_summary)
    except Exception as e:
        logger.error(f'Error in Extracting summaries for user_id {user_id} : {e}')
        error_response = validator_models.ErrorResponse(
            error="Error in extracting summaries",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )
    
    response = validator_models.GetSummariesResponse(
        page=page,
        offset=offset,
        user_id=user_id,
        summaries=extracted_summary
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump()
    )

@router.delete('/remove/{summary_id}')
def remove_summary(request: Request, summary_id: int):
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

    user_id = request.state.user.id
    try:
        with request.state.db() as session:
            extracted_summary = session.query(db_models.Summary).filter(db_models.Summary.user_id == user_id, db_models.Summary.id == summary_id, db_models.Summary.is_deleted == False).first()
    except Exception as e:
        logger.error(f'Error in Extracting summaries for user_id {user_id} : {e}')
        error_response = validator_models.ErrorResponse(
            error="Error in extracting summaries",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )
    
    if extracted_summary is None:
        error_response = validator_models.ErrorResponse(
            error=f"Summary does not exists with id {summary_id}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )

    try:
        # Mark Summary as Deleted
        with request.state.db() as session:
            extracted_summary.is_deleted = True
            extracted_summary.deleted_at = datetime.now()
            session.add(extracted_summary) 
            session.commit()
            session.refresh(extracted_summary)
            logger.info(f"Summary with id {summary_id} has been deleted by user {user_id}")

    except Exception as e:
        logger.error(f'Error in deleting summary with id {summary_id} : {e}')
        session.rollback()
        error_response = validator_models.ErrorResponse(
            error=f"Error in summary deletion",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'msg': f'Summary with id {summary_id} has been deleted'
        }
    )