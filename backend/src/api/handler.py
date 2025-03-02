import logging
from uuid import UUID
from fastapi import APIRouter


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


router = APIRouter()


@router.post("/create_question")
async def create_question():
    """
    Create questions from input content.
    """
    return {"message": "Hello, World from FastAPI"}


@router.post("/correction")
async def correction():
    """
    Correction user's answer
    """
    pass


@router.get("/result/{uuid}")
async def get_result(uuid: UUID):
    """
    Get user's test result
    """
    pass
