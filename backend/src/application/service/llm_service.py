from typing import Any

from langsmith import Client

from config.settings import settings


SYSTEM_PROMPT_TITLE = "readum-system-prompt"


def get_prompt_from_hub() -> Any:
    """hubからプロンプトテンプレートを取得する関数"""
    client = Client(api_key=settings.lang_chain.LANGCHAIN_API_KEY)
    return client.pull_prompt(SYSTEM_PROMPT_TITLE)
