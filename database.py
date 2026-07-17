from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///./avatar.db", 
                       connect_args={
                           "check_same_thread": False
                       })

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

"""
`Declarative` is thr foudantional base class used to create a central
registry for all SQLalchemy ORM models. Every database table class
inherit from it, acting as a "container" or "module" that groups
models together.
"""
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()