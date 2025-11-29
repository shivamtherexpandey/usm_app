from async_tasks.celery_init import celery_app
from utility import database_helper
from models import db_models
from sqlalchemy import select
from utility import logger
from summarization_tools import SummaryTool


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def generate_summary(self, summary_id: int) -> None:
    db_session = database_helper.SessionLocal()
    logger.info(f"Request received to generate summary for id {summary_id}")

    # Extract Summary object
    try:
        summary_object = db_session.execute(
            select(db_models.Summary).where(db_models.Summary.id == summary_id).limit(1)
        ).first()
        if summary_object is None:
            raise Exception()

        logger.info("Extracted summary object")
    except Exception as e:
        logger.error(f"Error {e}")
        logger.error(f"No summary object exists with id {summary_id}")
        db_session.close()
        raise self.retry(exc=e)

    summary_object = summary_object[0]

    if summary_object.processed:
        logger.info(
            f"Summary already processed for id {summary_id}, skipping generation"
        )
        return

    url = summary_object.url

    # Generate Summary
    summarizer = SummaryTool(url)
    summary_text = summarizer.summarize()

    try:
        # Update and Save Summary Object
        summary_object.summary = summary_text
        summary_object.processed = True

        db_session.add(summary_object)
        db_session.commit()
        db_session.refresh(summary_object)

    except Exception as e:
        logger.error(f"Error in saving summary with id {summary_id} : {e}")
        db_session.rollback()
        db_session.close()
        raise self.retry(exc=e)

    logger.info(f"Generated summary for id {summary_id}")
    db_session.close()
    return
