from fastapi import APIRouter, Depends, UploadFile, HTTPException, Path as FastAPIPath, Body
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db
from ..models import File, Note, Paragraph
from ..schemas import FileRead, RenameRequest
from ..services.llama_parse import parse_to_markdown
from datetime import datetime
import shutil
from fastapi.responses import JSONResponse
from ..config import FILENAME_REGEX, TEMP_DIR, logger

router = APIRouter()

# Regular expression pattern for validating filenames
FILENAME_REGEX = r"^[a-zA-Z0-9_\-\. ]+$"


@router.post("/markdown/{filename}")
def get_markdown_from_db(
    filename: str = FastAPIPath(..., regex=FILENAME_REGEX),
    db: Session = Depends(get_db)
):
    """
    Retrieve markdown content for a given filename from the database.

    Args:
        filename (str): The name of the file to retrieve.
        db (Session): Database session dependency.

    Returns:
        JSONResponse: JSON containing the file content.

    Raises:
        HTTPException: If the file is not found.
    """
    file = db.query(File).filter(File.filename == filename).first()
    if file:
        return JSONResponse(content={"content": file.content})
    else:
        logger.warning(f"Markdown content for {filename} not found in DB.")
        raise HTTPException(status_code=404, detail="File not found")


@router.get("", response_model=List[FileRead])
def list_files(db: Session = Depends(get_db)):
    """
    List all markdown files in the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[FileRead]: A list of file records.

    Raises:
        HTTPException: If an internal server error occurs.
    """
    try:
        files = db.query(File).all()
        logger.info(f"Listing all markdown files: {
                    [file.filename for file in files]}")
        return files
    except Exception as e:
        logger.error(f"Error fetching files: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{filename}", response_model=FileRead)
def get_file(filename: str = FastAPIPath(..., regex=FILENAME_REGEX), db: Session = Depends(get_db)):
    """
    Retrieve a specific file by filename.

    Args:
        filename (str): The name of the file to retrieve.
        db (Session): Database session dependency.

    Returns:
        FileRead: The file record.

    Raises:
        HTTPException: If the file is not found.
    """
    file = db.query(File).filter(File.filename == filename).first()
    if file:
        # Load paragraphs to ensure relationships are loaded
        file.paragraphs
        logger.info(f"Retrieved file {filename} from DB.")
        return file
    else:
        logger.warning(f"File {filename} not found in DB.")
        raise HTTPException(status_code=404, detail="File not found")


@router.patch("/{filename}/rename", response_model=FileRead)
def rename_file(
    filename: str = FastAPIPath(..., regex=FILENAME_REGEX),
    rename_request: RenameRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    Rename an existing file.

    Args:
        filename (str): The current name of the file.
        rename_request (RenameRequest): The new filename.
        db (Session): Database session dependency.

    Returns:
        FileRead: The updated file record.

    Raises:
        HTTPException: If the new filename is invalid or already exists.
    """
    new_filename_str = rename_request.new_filename
    if not new_filename_str:
        logger.warning("New filename was not provided.")
        raise HTTPException(
            status_code=400, detail="New filename is required.")

    # Check for unauthorized special characters
    forbidden_chars = [')', '#', '?', '&', '/', '*', '<', '>', '|', '\\']
    if any(char in new_filename_str for char in forbidden_chars):
        logger.warning(f"Unauthorized special characters in the filename: {
                       new_filename_str}")
        raise HTTPException(
            status_code=400,
            detail="The filename must not contain special characters such as ), #, ?, &, /."
        )

    logger.info(f"Attempting to rename file from {
                filename} to {new_filename_str}")

    # Check if the new filename already exists
    existing_file = db.query(File).filter(
        File.filename == new_filename_str).first()
    if existing_file:
        logger.warning(f"File with name {new_filename_str} already exists.")
        raise HTTPException(status_code=400, detail="File name already taken.")

    # Find the file to rename
    file = db.query(File).filter(File.filename == filename).first()
    if not file:
        logger.warning(f"File {filename} not found for renaming.")
        raise HTTPException(status_code=404, detail="File not found.")

    # Update the filename and timestamp
    old_filename = file.filename
    file.filename = new_filename_str
    file.updated_at = datetime.utcnow()  # Manually setting the updated_at
    db.commit()
    db.refresh(file)
    logger.info(f"File renamed from {old_filename} to {new_filename_str}.")
    print(f"File renamed from {old_filename} to {new_filename_str}.")

    # Log created_at and updated_at
    print(f"created_at: {file.created_at}, updated_at: {file.updated_at}")
    logger.info(f"created_at: {file.created_at}, updated_at: {
                file.updated_at}")

    return file


@router.delete("/{filename}")
def delete_file(filename: str = FastAPIPath(..., regex=FILENAME_REGEX), db: Session = Depends(get_db)):
    """
    Delete a file and its associated paragraphs and notes.

    Args:
        filename (str): The name of the file to delete.
        db (Session): Database session dependency.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the file is not found.
    """
    print(f"Received delete request for: {filename}")  # Debugging output
    logger.info(f"Attempting to delete file: {filename}")

    file = db.query(File).filter(File.filename == filename).first()
    if not file:
        logger.warning(f"File {filename} not found for deletion.")
        raise HTTPException(status_code=404, detail="File not found.")

    # Delete associated paragraphs and notes
    paragraphs = db.query(Paragraph).filter(Paragraph.file_id == file.id).all()
    for paragraph in paragraphs:
        db.query(Note).filter(Note.paragraph_id == paragraph.id).delete()
    db.query(Paragraph).filter(Paragraph.file_id == file.id).delete()

    db.delete(file)
    db.commit()
    logger.info(f"Deleted file {
                filename} and its associated paragraphs and notes from DB.")
    print(f"Deleted file {
          filename} and its associated paragraphs and notes from DB.")
    return {"detail": "File and associated paragraphs and notes deleted successfully."}


@router.post("/upload", response_model=List[FileRead])
async def upload_files(files: List[UploadFile], db: Session = Depends(get_db)):
    """
    Upload and process multiple files.

    Args:
        files (List[UploadFile]): List of files to upload.
        db (Session): Database session dependency.

    Returns:
        List[FileRead]: List of processed file records.

    Raises:
        HTTPException: If no files are received or processed successfully.
    """

    if not files:
        logger.warning("No files received for upload.")
        raise HTTPException(
            status_code=400, detail="No files received for upload.")

    processed_files = []

    for uploaded_file in files:
        try:
            # Check for unauthorized special characters in filename
            forbidden_chars = [')', '#', '?', '&',
                               '/', '*', '<', '>', '|', '\\']
            if any(char in uploaded_file.filename for char in forbidden_chars):
                logger.warning(f"Unauthorized special characters in the filename: {
                               uploaded_file.filename}")
                raise HTTPException(
                    status_code=400,
                    detail=f"The filename '{
                        uploaded_file.filename}' must not contain special characters such as ), #, ?, &, /."
                )

            # Validate file extension
            allowed_extensions = {"pdf", "docx"}
            file_extension = uploaded_file.filename.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                logger.warning(f"Unsupported file type: {
                               uploaded_file.filename}")
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {
                                    uploaded_file.filename}")

            # Temporarily save the uploaded file
            temp_file_path = TEMP_DIR / uploaded_file.filename
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(uploaded_file.file, buffer)
            logger.info(f"File {uploaded_file.filename} temporarily saved.")

            # Create a new File entry in the database
            new_file = File(
                filename=uploaded_file.filename,  # Preserve the full filename
                content=""  # To be updated later
            )
            db.add(new_file)
            db.commit()
            db.refresh(new_file)

            # Process the file with llama_parse
            parse_result = await parse_to_markdown(str(temp_file_path), db, new_file.id, new_file.filename)
            if parse_result is None:
                logger.warning(f"No documents in file {
                               uploaded_file.filename} found.")
                db.delete(new_file)
                db.commit()
                continue  # Skip if no documents are found

            filename = parse_result["filename"]
            content = parse_result["content"]
            paragraph_ids = parse_result.get("paragraph_ids", [])

            # Update the file content with parsed paragraphs
            new_file.content = content
            db.commit()
            db.refresh(new_file)
            logger.info(f"File {filename} created and parsed.")

            processed_files.append(new_file)

            # Remove the temporary file
            temp_file_path.unlink()
            logger.info(f"Temporary file {uploaded_file.filename} deleted.")

        except HTTPException as he:
            logger.error(f"HTTP error while processing the file {
                         uploaded_file.filename}: {he.detail}")
            raise he
        except Exception as e:
            logger.error(f"Error processing the file {
                         uploaded_file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing the file {
                                uploaded_file.filename}.")

    if not processed_files:
        logger.warning("No files processed successfully.")
        raise HTTPException(
            status_code=400, detail="No files processed successfully.")

    return processed_files
