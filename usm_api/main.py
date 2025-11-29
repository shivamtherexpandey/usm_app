from fastapi import FastAPI
from config import Config
from utility import logger
from routes import summarizer_router
from middlewares import AuthMiddleware, DBSessionMiddleware, CORSMiddleware
from exceptions import register_exception_handlers

app = FastAPI(prefix='/usm')

# Add Middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(DBSessionMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=Config.CORS_ALLOWED_ORIGINS, allow_credentials=True, allow_headers=['*'], allow_methods=['*'])

# Add Routes
app.include_router(summarizer_router, prefix='/summarizer')

# Add Global Exception Handlers
register_exception_handlers(app)