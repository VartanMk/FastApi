from sqlalchemy import Column, Integer, String, ForeignKey, Date, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DB_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/mydatabase"
Base = declarative_base()
engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Document(Base):
    __tablename__ = 'Document'
    id_Document = Column(Integer, primary_key=True, autoincrement=True)
    psth = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    text = relationship('Document_text', back_populates='document', uselist=False)


class Document_text(Base):
    __tablename__ = 'Document_text'
    id_Document_text = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    id_Document = Column(Integer, ForeignKey('Document.id_Document', ondelete="CASCADE"), nullable=False)
    document = relationship('Document', back_populates='text')
