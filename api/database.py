import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""Configure database access, see https://fastapi.tiangolo.com/tutorial/sql-databases/"""

SQLALCHEMY_DATABASE_URL = os.environ.get('DB_ENDPOINT')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
