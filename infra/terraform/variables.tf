variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "storage_bucket_name" {
  description = "Cloud Storageバケット名"
  type        = string
}

variable "service_account_id" {
  description = "サービスアカウントID（@より前の部分）"
  type        = string
}

variable "service_account_display_name" {
  description = "サービスアカウントの表示名"
  type        = string
  default     = "Readum Service Account"
}

variable "network_name" {
  description = "VPCネットワーク名"
  type        = string
  default     = "vpc-network"
}

variable "connector_name" {
  description = "VPCアクセスコネクタ名"
  type        = string
  default     = "vpc-connector"
}

variable "frontend_service_name" {
  description = "フロントエンドのCloud Run名"
  type        = string
  default     = "readum_frontend"
}

variable "backend_service_name" {
  description = "バックエンドのCloud Run名"
  type        = string
  default     = "readum_backend"
}

variable "storage_roles" {
  description = "ストレージに付与するロール一覧"
  type        = list(string)
  default     = ["roles/storage.admin"]
}

###########################################################
# 環境変数の設定
###########################################################
variable "NEXT_PUBLIC_API_URL" {
  description = "バックエンドのAPIエンドポイント"
  type        = string
}
variable "NEXT_PUBLIC_MAX_QUESTION_COUNT" {
  description = "フロントエンド側で生成できる問題数の上限値"
  type        = number
  default     = 10
}
variable "NEXT_PUBLIC_MIN_QUESTION_COUNT" {
  description = "フロントエンド側で生成できる問題数の最低値"
  type        = number
  default     = 3
}
variable "NEXT_PUBLIC_DISABLED_CRAWL" {
  description = "クローリング機能をdisabledにするかどうか"
  type        = bool
  default     = true
}

variable "ENV" {
  description = "実行環境 (dev/stg/prd)"
  type        = string
  default     = "prd" # デフォルト値を設定
}

variable "ALLOW_ORIGIN" {
  description = "CORS許可オリジン"
  type        = string
  default     = "*" # デフォルト値を設定
}

variable "GPT_MODEL" {
  description = "GPTモデル名"
  type        = string
  default     = "gpt-4o-mini" # デフォルト値を設定
}

variable "TEXT_EMBEDDINGS_MODEL" {
  description = "テキスト埋め込みモデル"
  type        = string
  default     = "text-embedding-3-small" # デフォルト値を設定
}

variable "additional_env_vars" {
  description = "追加の環境変数"
  type        = map(string)
  default = {
    TMP_VECTORDB_PATH              = "assets/tmp/"
    VECTORDB_PROVIDER              = "faiss"
    SEARCH_KWARGS                  = "8"
    CHUNK_SIZE                     = "2000"
    CHUNK_OVERLAP                  = "100"
    GOOGLE_APPLICATION_CREDENTIALS = "./credential.json"
  }
}
