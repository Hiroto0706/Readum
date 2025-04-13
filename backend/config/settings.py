from typing import Final
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, field_validator
import os

load_dotenv()


class AppSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    ENV: Final[str] = os.getenv("ENV", "dev")
    ALLOW_ORIGIN: Final[str] = os.getenv("ALLOW_ORIGIN")

    DEBUG_LEV: int = 10
    INFO_LEV: int = 20
    LOG_LEVEL: Final[int] = DEBUG_LEV if ENV == "dev" else INFO_LEV


# TODO: APIのバリデーションはあったほうがいい
class LLMSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    OPENAI_API_KEY: Final[str] = Field(default=os.getenv("OPENAI_API_KEY"))

    @field_validator("OPENAI_API_KEY", check_fields=False)
    def validate_openai_api_key(cls, v: str) -> str:
        if not v:
            raise ValueError("OPENAI_API_KEY is not set")
        return v


class ModelSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    GPT_MODEL: Final[str] = os.getenv("GPT_MODEL")
    TEXT_EMBEDDINGS_MODEL: Final[str] = os.getenv("TEXT_EMBEDDINGS_MODEL")


class LangChainSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    LANGCHAIN_API_KEY: Final[str] = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: Final[str] = os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT: Final[str] = os.getenv("LANGCHAIN_PROJECT")


class EmbeddingsSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    TMP_VECTORDB_PATH: Final[str] = os.getenv("TMP_VECTORDB_PATH")
    VECTORDB_PROVIDER: Final[str] = os.getenv("VECTORDB_PROVIDER")
    SEARCH_KWARGS: Final[int] = int(os.getenv("SEARCH_KWARGS", 8))


class TextSplitterSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    CHUNK_SIZE: Final[int] = int(os.getenv("CHUNK_SIZE", 2000))
    CHUNK_OVERLAP: Final[int] = int(os.getenv("CHUNK_OVERLAP", 100))


class TestSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    DOC_PATH: Final[str] = os.getenv("DOC_PATH")


class ThirdPartySettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    FIRECRAWL_API_KEY: Final[str] = os.getenv("FIRECRAWL_API_KEY")
    BUCKET_NAME: Final[str] = os.getenv("BUCKET_NAME")


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True)

    app: AppSettings = Field(default_factory=AppSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    model: ModelSettings = Field(default_factory=ModelSettings)
    embeddings: EmbeddingsSettings = Field(default_factory=EmbeddingsSettings)
    lang_chain: LangChainSettings = Field(default_factory=LangChainSettings)
    text_splitter: TextSplitterSettings = Field(default_factory=TextSplitterSettings)
    test: TestSettings = Field(default_factory=TestSettings)
    third_party: ThirdPartySettings = Field(default_factory=ThirdPartySettings)


settings = Settings()
