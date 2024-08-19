from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from environment import SQLALCHEMY_DB_URL
from fastapi import Request

engine = create_engine(SQLALCHEMY_DB_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

class DBSession(Session):
    def __init__(self):
        super().__init__(bind=engine, autocommit=False, autoflush=False)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def get_session(request: Request) -> Session:
    return request.state.db

def with_db_session(func):
    def wrapper(*arg, **kwargs):
        # Check if db is passed as a keyword argument
        if 'db' in kwargs:
            return func(*arg, **kwargs)
        
        for a in arg:
            if isinstance(a, Session):
                return func(*arg, **kwargs)
        
        # Otherwise, create a new session
        with DBSession() as db:
            return func(*arg, db=db, **kwargs)
        
    return wrapper