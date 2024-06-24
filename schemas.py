








# from pydantic import BaseModel
# from datetime import date
# from typing import List
#
# class DocumentBase(BaseModel):
#     psth: str
#     date: date
#
# class DocumentCreate(DocumentBase):
#     pass
#
# class Document(DocumentBase):
#     id_Document: int
#     texts: List[int]
#
#    ## class Config:
#      ##   orm_mode = True
#
# class DocumentTextBase(BaseModel):
#     text: str
#
# class DocumentTextCreate(DocumentTextBase):
#     pass
#
# class DocumentText(DocumentTextBase):
#     id_Document_text: int
#     documents: List[int]
#
#     # class Config:
#     #     orm_mode = True
#
