from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Document_text, Document, DB_URL

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def create_database():
    Base.metadata.create_all(bind=engine)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

create_database()
