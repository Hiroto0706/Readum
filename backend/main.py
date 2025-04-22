import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import quiz_router, result_router
from config.settings import settings

load_dotenv()


logging.basicConfig(
    level=settings.app.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[settings.app.ALLOW_ORIGIN],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/api/v1/quiz")
app.include_router(result_router, prefix="/api/v1/result")


@app.get("/")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    print("Hello Readum Project!!")
