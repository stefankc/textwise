"""
Database models for the application.

This module defines the SQLAlchemy ORM models that represent the database structure.
Contains models for Files, Paragraphs, and their relationships.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class File(Base):
    """
    Represents a file in the system.

    Attributes:
        id (int): Primary key identifier
        filename (str): Unique name of the file
        content (str): Content of the file
        created_at (datetime): Timestamp of file creation
        updated_at (datetime): Timestamp of last update
        paragraphs (relationship): One-to-many relationship with Paragraph model
    """
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(
    ), server_default=func.now(), nullable=False)

    # Beziehungen zu Paragraph und anderen Modellen
    paragraphs = relationship("Paragraph", back_populates="file")


class Paragraph(Base):
    """
    Represents a paragraph in a file.
    Attributes:
        id (int): Primary key identifier.
        file_id (int): Foreign key referencing the associated file.
        order (int): The order of the paragraph within the file.
        content (str): The text content of the paragraph.
        created_at (datetime): Timestamp when the paragraph was created.
        updated_at (datetime): Timestamp when the paragraph was last updated.
        notes (relationship): Relationships to Note objects associated with the paragraph.
        file (relationship): Relationship to the File object this paragraph belongs to.
    """
    __tablename__ = 'paragraphs'

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    order = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(
    ), server_default=func.now(), nullable=False)

    # Beziehungen zu Note
    notes = relationship("Note", back_populates="paragraph")
    file = relationship("File", back_populates="paragraphs")


class Note(Base):
    """
    Represents a note/annotation for a paragraph.

    Attributes:
        id (int): Primary key identifier
        paragraph_id (int): Foreign key referencing the associated paragraph
        content (str): Content of the note
        created_at (datetime): Timestamp of note creation
        updated_at (datetime): Timestamp of last update
        paragraph (relationship): Many-to-one relationship with Paragraph model
    """
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    paragraph_id = Column(Integer, ForeignKey('paragraphs.id'), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(
    ), server_default=func.now(), nullable=False)

    # Beziehungen zu Paragraph
    paragraph = relationship("Paragraph", back_populates="notes")


class APIKey(Base):
    """
    Represents an API key for external services.

    Attributes:
        id (int): Primary key identifier
        service (str): Name of the service (e.g., 'openai', 'llama_cloud')
        key (str): The API key value
    """
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    # z.B. 'openai', 'llama_cloud'
    service = Column(String, unique=True, index=True)
    key = Column(String, nullable=False)
