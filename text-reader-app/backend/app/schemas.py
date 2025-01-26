from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class RenameRequest(BaseModel):
    new_filename: str

    class Config:
        from_attributes = True


class ParagraphBase(BaseModel):
    order: int
    content: str


class ParagraphRead(ParagraphBase):
    id: int
    file_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    paragraph_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Anstelle von orm_mode = True


class FileBase(BaseModel):
    filename: str


class FileCreate(FileBase):
    content: str


class FileRead(FileBase):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    paragraphs: List[ParagraphRead] = []

    class Config:
        from_attributes = True  # Anstelle von orm_mode = True


class QueryRequest(BaseModel):
    paragraph_id: int
    context: str
    note_content: str  # Notizinhalt


class QueryResponse(BaseModel):
    feedback: str  # Korrekt auf 'feedback' gesetzt


class APIKeys(BaseModel):
    OPENAI_API_KEY: str = Field(..., title="OpenAI API Key")
    LLAMA_CLOUD_API_KEY: str = Field(..., title="LLAMA Cloud API Key")
