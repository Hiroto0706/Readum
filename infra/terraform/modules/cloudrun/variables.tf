variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
}

variable "frontend_service_name" {
  description = "フロントエンドのCloud Run名"
  type        = string
}

variable "backend_service_name" {
  description = "バックエンドのCloud Run名"
  type        = string
}

variable "service_account_email" {
  description = "サービスアカウントのメールアドレス"
  type        = string
}

variable "vpc_connector_id" {
  description = "VPCアクセスコネクタのID"
  type        = string
}

###########################################################
# 環境変数の設定
###########################################################
variable "API_ENDPOINT" {
  description = "バックエンドのAPIエンドポイント"
  type        = string
}
variable "NEXT_PUBLIC_MAX_QUESTION_COUNT" {
  description = "フロントエンド側で生成できる問題数の上限値"
  type        = number
}
variable "NEXT_PUBLIC_MIN_QUESTION_COUNT" {
  description = "フロントエンド側で生成できる問題数の最低値"
  type        = number
}
variable "DISABLED_CRAWL" {
  description = "クローリング機能をdisabledにするかどうか"
  type        = bool
}

variable "ENV" {
  description = "実行環境 (dev/stg/prd)"
  type        = string
}

variable "ALLOW_ORIGIN" {
  description = "CORS許可オリジン"
  type        = string
}

variable "GPT_MODEL" {
  description = "GPTモデル名"
  type        = string
}

variable "TEXT_EMBEDDINGS_MODEL" {
  description = "テキスト埋め込みモデル"
  type        = string
}

variable "additional_env_vars" {
  description = "追加の環境変数"
  type        = map(string)
}
