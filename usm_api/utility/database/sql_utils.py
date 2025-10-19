import os
from typing import Generator
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from config import Config

engine = create_engine(Config.SQL_DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_sql_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()