from dotenv import load_dotenv
from pydantic.dataclasses import dataclass
import os

load_dotenv()


@dataclass(frozen=True)
class AppSettings:
    ENV: str = os.getenv("ENV", "dev")
    ALLOW_ORIGIN: str = os.getenv("ALLOW_ORIGIN")

    _DEBUG_LEV = 10
    _INFO_LEV = 20
    LOG_LEVEL: int = _DEBUG_LEV if ENV == "dev" else _INFO_LEV


# TODO: APIのバリデーションはあったほうがいい
@dataclass(frozen=True)
class LLMSettings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


@dataclass(frozen=True)
class ModelSettings:
    GPT_MODEL: str = os.getenv("GPT_MODEL")
    TEXT_EMBEDDINGS_MODEL: str = os.getenv("TEXT_EMBEDDINGS_MODEL")


@dataclass(frozen=True)
class LangChainSettings:
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT")


@dataclass(frozen=True)
class EmbeddingsSettings:
    TMP_VECTORDB_PATH: str = os.getenv("TMP_VECTORDB_PATH")
    VECTORDB_PROVIDER: str = os.getenv("VECTORDB_PROVIDER")


@dataclass(frozen=True)
class TextSplitterSettings:
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 2000))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 100))


@dataclass(frozen=True)
class TestSettings:
    DOC_PATH: str = os.getenv("DOC_PATH")


@dataclass(frozen=True)
class ThirdPartySettings:
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY")


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
