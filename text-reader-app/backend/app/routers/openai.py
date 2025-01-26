from fastapi import APIRouter, Depends, HTTPException
from ..schemas import QueryRequest, QueryResponse
from ..services.openai_service import OpenAIService  # Import OpenAIService

from ..config import logger 


router = APIRouter()

def get_openai_service():
    return OpenAIService()


@router.post("/get_feedback", response_model=QueryResponse)
def ask_openai_feedback(query: QueryRequest, openai_service: OpenAIService = Depends(get_openai_service)):
    """
    Handle POST requests to generate feedback using OpenAI.

    Args:
        query (QueryRequest): The request containing context, note content, and paragraph ID.
        openai_service (OpenAIService, optional): Service to interact with OpenAI API. Defaults to Depends(get_openai_service).

    Returns:
        QueryResponse: The response containing the generated feedback.

    Raises:
        HTTPException: If there is an error during the request to OpenAI.
    """
    try:
        feedback = openai_service.get_feedback(
            context=query.context,
            note_content=query.note_content,
            paragraph_id=query.paragraph_id
        )
        logger.info("Feedback successfully generated")
        return QueryResponse(feedback=feedback)
    except Exception as e:
        logger.error(f"Error in the request to OpenAI: {e}")
        raise HTTPException(
            status_code=500, detail="Error in the request to OpenAI.")
