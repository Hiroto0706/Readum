from fastapi import APIRouter
from src.api.handler import router as api_router


router = APIRouter()

router.include_router(api_router, prefix="/v1")
