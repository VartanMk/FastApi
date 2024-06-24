import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from models import Document, Document_text
from database import get_db
from celery_worker import analyse_document


BASEDIR = os.path.dirname(__file__)
app = FastAPI()

DESKTOP_PATH = "/home/vartan/Рабочий стол/document/"


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.post('/upload_doc')
def up_file(file: UploadFile = File(...), session: Session = Depends(get_db)):
    if file is None or file.filename is None:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_path = os.path.join(DESKTOP_PATH, file.filename)

    # Запись файла на диск
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    db_document = Document(psth=os.path.join(DESKTOP_PATH, file.filename), date=datetime.now())
    session.add(db_document)
    session.commit()

    return {"message": f"{file.filename} id {db_document.id_Document}"}


@app.delete("/doc_delete/{id_Document}")
def delete_doc(id_Document: int, db: Session = Depends(get_db)):
    """Удаление документа по его идентификатору"""
    document = db.query(Document).filter(Document.id_Document == id_Document).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(document)
    db.commit()

    return {"message": "Document deleted"}


@app.post("/doc_analyse/{document_id}")
def analyse_doc(document_id: int):
    analyse_document.delay(document_id)
    return {"message": "Document analysis started"}


@app.get("/get_text/{document_id}")
def get_text(document_id: int, session: Session = Depends(get_db)):
    document_text = session.query(Document_text).filter(Document_text.id_Document == document_id).first()
    if not document_text:
        raise HTTPException(status_code=404, detail="Document text not found")

    return {"document_text": document_text.text}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
