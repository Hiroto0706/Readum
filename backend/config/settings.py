from typing import Final
from dotenv import load_dotenv
from pydantic.dataclasses import dataclass
import os

load_dotenv()


@dataclass(frozen=True)
class AppSettings:
    ENV: Final[str] = os.getenv("ENV", "dev")
    ALLOW_ORIGIN: Final[str] = os.getenv("ALLOW_ORIGIN")

    DEBUG_LEV = 10
    INFO_LEV = 20
    LOG_LEVEL: Final[int] = DEBUG_LEV if ENV == "dev" else INFO_LEV


# TODO: APIのバリデーションはあったほうがいい
@dataclass(frozen=True)
class LLMSettings:
    OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY")

    def __post_init__(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")


@dataclass(frozen=True)
class ModelSettings:
    GPT_MODEL: Final[str] = os.getenv("GPT_MODEL")
    TEXT_EMBEDDINGS_MODEL: Final[str] = os.getenv("TEXT_EMBEDDINGS_MODEL")


@dataclass(frozen=True)
class LangChainSettings:
    LANGCHAIN_API_KEY: Final[str] = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: Final[str] = os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT: Final[str] = os.getenv("LANGCHAIN_PROJECT")


@dataclass(frozen=True)
class EmbeddingsSettings:
    TMP_VECTORDB_PATH: Final[str] = os.getenv("TMP_VECTORDB_PATH")
    VECTORDB_PROVIDER: Final[str] = os.getenv("VECTORDB_PROVIDER")
    SEARCH_KWARGS: Final[int] = int(os.getenv("SEARCH_KWARGS", 8))


@dataclass(frozen=True)
class TextSplitterSettings:
    CHUNK_SIZE: Final[int] = int(os.getenv("CHUNK_SIZE", 2000))
    CHUNK_OVERLAP: Final[int] = int(os.getenv("CHUNK_OVERLAP", 100))


@dataclass(frozen=True)
class TestSettings:
    DOC_PATH: Final[str] = os.getenv("DOC_PATH")


@dataclass(frozen=True)
class ThirdPartySettings:
    FIRECRAWL_API_KEY: Final[str] = os.getenv("FIRECRAWL_API_KEY")


@dataclass(frozen=True)
class Settings:
    app: AppSettings = AppSettings()
    llm: LLMSettings = LLMSettings()
    model: ModelSettings = ModelSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    lang_chain: LangChainSettings = LangChainSettings()
    text_splitter: TextSplitterSettings = TextSplitterSettings()
    test: TestSettings = TestSettings()
    third_party: ThirdPartySettings = ThirdPartySettings()


settings = Settings()
