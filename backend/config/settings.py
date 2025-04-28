from typing import ClassVar
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, field_validator
import os

load_dotenv()


class AppSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    ENV: ClassVar[str] = os.getenv("ENV", "dev")
    ALLOW_ORIGIN: ClassVar[str] = os.getenv("ALLOW_ORIGIN")

    DEBUG_LEV: int = 10
    INFO_LEV: int = 20
    LOG_LEVEL: ClassVar[int] = DEBUG_LEV if ENV == "dev" else INFO_LEV

    # LangGraphを用いてクイズを生成するかどうか
    USE_LANGGRAPH: ClassVar[bool] = os.getenv("USE_LANGGRAPH", "false") == "true"


# TODO: APIのバリデーションはあったほうがいい
class LLMSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    OPENAI_API_KEY: ClassVar[str] = Field(default=os.getenv("OPENAI_API_KEY"))

    @field_validator("OPENAI_API_KEY", check_fields=False)
    def validate_openai_api_key(cls, v: str) -> str:
        if not v:
            raise ValueError("OPENAI_API_KEY is not set")
        return v


class ModelSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    GPT_MODEL: ClassVar[str] = os.getenv("GPT_MODEL")
    TEXT_EMBEDDINGS_MODEL: ClassVar[str] = os.getenv("TEXT_EMBEDDINGS_MODEL")


class LangChainSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    LANGCHAIN_API_KEY: ClassVar[str] = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: ClassVar[str] = os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT: ClassVar[str] = os.getenv("LANGCHAIN_PROJECT")


class EmbeddingsSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    TMP_VECTORDB_PATH: ClassVar[str] = os.getenv("TMP_VECTORDB_PATH")
    VECTORDB_PROVIDER: ClassVar[str] = os.getenv("VECTORDB_PROVIDER")
    SEARCH_KWARGS: ClassVar[int] = int(os.getenv("SEARCH_KWARGS", 8))


class TextSplitterSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    CHUNK_SIZE: ClassVar[int] = int(os.getenv("CHUNK_SIZE", 2000))
    CHUNK_OVERLAP: ClassVar[int] = int(os.getenv("CHUNK_OVERLAP", 100))


class TestSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    DOC_PATH: ClassVar[str] = os.getenv("DOC_PATH")


class ThirdPartySettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    FIRECRAWL_API_KEY: ClassVar[str] = os.getenv("FIRECRAWL_API_KEY")
    BUCKET_NAME: ClassVar[str] = os.getenv("BUCKET_NAME")


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
