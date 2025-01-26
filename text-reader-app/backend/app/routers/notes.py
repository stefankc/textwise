# backend/app/routers/notes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db
from ..models import Note, File, Paragraph
from ..schemas import NoteRead, NoteCreate
import logging
from ..config import logger  # Import logger configuration

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/file_by_name/{filename}", response_model=List[NoteRead])
def get_notes_for_file_by_name(filename: str, db: Session = Depends(get_db)):
    """
    Retrieve all notes associated with a specific file by its filename.

    Args:
        filename (str): The name of the file.
        db (Session): Database session dependency.

    Returns:
        List[NoteRead]: A list of notes for the specified file.
    """
    file = db.query(File).filter(File.filename == filename).first()
    if not file:
        logger.warning(f"File {filename} not found when fetching notes.")
        raise HTTPException(status_code=404, detail="File not found")

    paragraphs = db.query(Paragraph).filter(
        Paragraph.file_id == file.id).order_by(Paragraph.order).all()
    paragraph_ids = [p.id for p in paragraphs]
    notes = db.query(Note).filter(Note.paragraph_id.in_(paragraph_ids)).all()
    return notes


@router.post("/{filename}/{paragraph_id}", response_model=NoteRead)
def create_note(filename: str, paragraph_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note for a specific paragraph in a file.

    Args:
        filename (str): The name of the file.
        paragraph_id (int): The ID of the paragraph.
        note (NoteCreate): The content of the note to create.
        db (Session): Database session dependency.

    Returns:
        NoteRead: The created note.
    """
    try:
        file = db.query(File).filter(File.filename == filename).first()
        if not file:
            logger.warning(f"File {filename} not found when creating a note.")
            raise HTTPException(status_code=404, detail="File not found")

        # Check if the paragraph exists and belongs to the file
        paragraph = db.query(Paragraph).filter(
            Paragraph.id == paragraph_id, Paragraph.file_id == file.id).first()
        if not paragraph:
            logger.warning(
                f"Paragraph {paragraph_id} not found in file {filename}.")
            raise HTTPException(
                status_code=404, detail="Paragraph not found in the specified file.")

        # Check if a note already exists for this paragraph
        existing_note = db.query(Note).filter(
            Note.paragraph_id == paragraph_id).first()
        if existing_note:
            logger.warning(f"Note for paragraph {paragraph_id} in file {
                           filename} already exists.")
            raise HTTPException(
                status_code=400, detail="Note already exists for this paragraph.")

        db_note = Note(
            paragraph_id=paragraph_id,
            content=note.content
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        logger.info(f"Created note for paragraph {
                    paragraph_id} in file {filename}.")
        return db_note
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    """
    Update an existing note by its ID.

    Args:
        note_id (int): The ID of the note to update.
        note (NoteCreate): The new content for the note.
        db (Session): Database session dependency.

    Returns:
        NoteRead: The updated note.
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        logger.warning(f"Note with id {note_id} not found for update.")
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    logger.info(f"Updated note {note_id}.")
    return db_note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note by its ID.

    Args:
        note_id (int): The ID of the note to delete.
        db (Session): Database session dependency.

    Returns:
        dict: Confirmation message of deletion.
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        logger.warning(f"Note with id {note_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    logger.info(f"Deleted note {note_id}.")
    return {"detail": "Note deleted successfully."}
