from fastapi.responses import Response
from fastapi.requests import Request
from fastapi import APIRouter

router = APIRouter(prefix='/summarizer', tags=['summarizer'])

@router.post('/summarize')
def summarize(request: Request):
    with request.state.db() as session:
        print('Session started')
    return Response(content="Summarization result")