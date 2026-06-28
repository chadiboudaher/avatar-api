from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./avatar.db"

# Open actual connection to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
'''
 A factory that create database sessions (think of a session as
 one conversation with the DB)
'''
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
'''
models inherit this (Base), it's how SQLAlchemy knows what to turn 
into tables.
'''
class Base(DeclarativeBase):
    pass