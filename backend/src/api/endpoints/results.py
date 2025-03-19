import logging
from uuid import UUID
from fastapi import APIRouter


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/result/{uuid}")
async def get_result(uuid: UUID):
    """
    Get user's test result
    """
    pass
