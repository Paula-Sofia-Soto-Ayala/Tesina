from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from llm_bias_study.db.models import Base

DATABASE_URL = "sqlite:///llm_bias_study.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()