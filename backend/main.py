import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import quiz_router, results_router
from config.settings import settings

load_dotenv()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = FastAPI()

# TODO: ここの設定詳しく見る必要あり
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app.ALLOW_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/api/v1/quiz")
app.include_router(results_router, prefix="/api/v1/results")


@app.get("/")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    print("Hello Readum Project!!")
