# APIキー関連のシークレット
module "secret_openai_api_key" {
  source    = "../secret_manager"
  secret_id = "readum_openai_api_key"
}

module "secret_langchain_api_key" {
  source    = "../secret_manager"
  secret_id = "readum_langchain_api_key"
}

module "secret_firecrawl_api_key" {
  source    = "../secret_manager"
  secret_id = "readum_firecrawl_api_key"
}

# シークレットの最新バージョンを取得
data "google_secret_manager_secret_version" "openai_api_key" {
  secret  = module.secret_openai_api_key.secret_id
  version = "latest"
}

data "google_secret_manager_secret_version" "langchain_api_key" {
  secret  = module.secret_langchain_api_key.secret_id
  version = "latest"
}

data "google_secret_manager_secret_version" "firecrawl_api_key" {
  secret  = module.secret_firecrawl_api_key.secret_id
  version = "latest"
}

# ローカル変数としてシークレット値を保持
locals {
  OPENAI_API_KEY    = data.google_secret_manager_secret_version.openai_api_key.secret_data
  LANGCHAIN_API_KEY = data.google_secret_manager_secret_version.langchain_api_key.secret_data
  FIRECRAWL_API_KEY = data.google_secret_manager_secret_version.firecrawl_api_key.secret_data
}
