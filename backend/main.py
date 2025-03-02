import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router as api_router

load_dotenv()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = FastAPI()

# TODO: ここの設定詳しく見る必要あり
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {"status": "OK"}


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    print("Hello Readum Project!!")
