from pathlib import Path
import logging
from ..crud import read_api_keys
from llama_parse import LlamaParse
from sqlalchemy.orm import Session
from ..models import Paragraph


async def parse_to_markdown(input_file: str, db: Session, file_id: int, filename: str) -> dict:
    """
    Parse the input file to markdown, create Paragraph entries in the database,
    and return relevant information.

    Args:
        input_file (str): Path to the input file to be parsed.
        db (Session): SQLAlchemy database session.
        file_id (int): ID of the associated File entry in the database.
        filename (str): Name of the file being processed.

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing filename, markdown content,
        and list of paragraph IDs if successful; otherwise, None.
    """
    try:
        # Reading the API keys from config.json
        api_keys = read_api_keys()
        if not api_keys:
            raise ValueError(
                "API keys are not set. Please enter the API keys in the settings.")

        llama_api_key = api_keys.LLAMA_CLOUD_API_KEY
        if not llama_api_key:
            raise ValueError("LLAMA_CLOUD_API_KEY is not set.")

        logging.info(f"Using LLAMA_CLOUD_API_KEY: {llama_api_key}")

        # Initializing LlamaParse with the API key from config.json
        parser = LlamaParse(
            api_key=llama_api_key,
            result_type="markdown",
            verbose=True
        )

        # Parsing the input file
        with open(input_file, "rb") as f:
            documents = await parser.aload_data(f, extra_info={"file_name": Path(input_file).name})

        # Check if documents were found
        if not documents:
            logging.warning(f"No documents found in file {filename}.")
            return None

        # Extracting the Markdown content from all pages
        markdown_content = "\n\n".join([doc.text for doc in documents])

        # Splitting the content into paragraphs
        paragraphs = markdown_content.split(
            '\n\n')  # Split by double line breaks
        processed_paragraphs = []
        buffer = ""

        for paragraph in paragraphs:
            if paragraph.startswith("#"):
                if buffer:
                    processed_paragraphs.append(buffer.strip())
                    buffer = ""
                processed_paragraphs.append(paragraph.strip())
            elif paragraph.endswith((".", "?", "!", ":")):
                buffer += ' ' + paragraph.strip()
                processed_paragraphs.append(buffer.strip())
                buffer = ""
            else:
                buffer += ' ' + paragraph.strip()

        if buffer:
            processed_paragraphs.append(buffer.strip())

        # Use processed_paragraphs instead of paragraphs
        paragraphs = processed_paragraphs

        # Storing the paragraphs in the database
        paragraph_ids = []
        db_paragraphs = []
        paragraph_order = 1

        for paragraph in paragraphs:
            db_paragraph = Paragraph(
                file_id=file_id,
                order=paragraph_order,
                content=paragraph
            )
            db_paragraphs.append(db_paragraph)
            paragraph_order += 1

        # Add all paragraphs at once and commit
        db.add_all(db_paragraphs)
        db.commit()

        # Update the IDs after the commit
        for db_paragraph in db_paragraphs:
            db.refresh(db_paragraph)
            paragraph_ids.append(db_paragraph.id)

        return {
            "filename": filename,
            "content": markdown_content,
            "paragraph_ids": paragraph_ids
        }
    except Exception as e:
        # Log the error and return None
        logging.error(f"Error parsing the file {input_file}: {e}")
        return None
