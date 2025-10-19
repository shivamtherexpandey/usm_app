from fastapi import FastAPI
from config import Config
from routes import summarizer_router
from middlewares import AuthMiddleware, DBSessionMiddleware
from exceptions import register_exception_handlers

app = FastAPI(prefix='/usm')

# Add Middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(DBSessionMiddleware)

# Add Routes
app.include_router(summarizer_router)

# Add Global Exception Handlers
register_exception_handlers(app)