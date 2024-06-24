
from celery import Celery
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from models import Document, Document_text
from database import DB_URL
from PIL import Image
import pytesseract


app = Celery('celery_worker', broker='pyamqp://guest:guest@localhost:5672//')
app.conf.broker_connection_retry_on_startup = True
app.conf.result_backend = 'rpc://'

app.autodiscover_tasks(["celery_worker"])

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


# @app.task
# def analyse_document(document_id: int, *args, **kwargs):
#     with SessionLocal() as session:
#         doc_path = session.query(Document.psth).filter(Document.id_Document == document_id).first()
#         if doc_path is None:
#             doc_text = session.query(Document_text).filter(Document_text.id_Document_text == document_id).one_or_none()
#             if doc_text is not None:
#                 reader = easyocr.Reader(['ru'])
#                 text = reader.readtext(doc_path.psth)  # Чтение текста
#                 text = " ".join(text)
#                 new_doc_text = Document_text(id_Document=document_id, text=text)
#                 session.add(new_doc_text)
#                 session.commit()
#
#             return {"message": "Документ обработан"}

@app.task
def analyse_document(document_id: int, *args, **kwargs):
    try:
        with SessionLocal() as session:
            doc_path = session.query(Document.psth).filter(Document.id_Document == document_id).first()
            if doc_path is not None:
                doc_text = session.query(Document_text).filter(Document_text.id_Document_text == document_id).one_or_none()
                if doc_text is None:
                    image = Image.open(doc_path)
                    text = pytesseract.image_to_string(image, lang='rus')
                    new_doc_text = Document_text(id_Document_text=document_id, text=text)
                    session.add(new_doc_text)
                    session.commit()
                return {"message": "Документ обработан"}
            else:
                return {"message": "Документ не найден"}

    except: FileNotFoundError("Файл не найден")



            # new_doc_text = Document_text(id_Document_text=document_id, text=recognized_text)
            # session.add(new_doc_text)
            # session.commit()

