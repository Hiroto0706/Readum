type UrlType = "client" | "server";

/**
 * 環境に基づいたベースURLを取得する
 * @param type - 'client' または 'server'
 * @returns ベースURL文字列
 */
export function getBaseUrl(type: UrlType = "server"): string {
  const env = process.env.NODE_ENV || "production";
  const isDev = env === "development";

  if (isDev) {
    if (type === "client") {
      return (
        process.env.NEXT_PUBLIC_API_URL_CLIENT ||
        "http://localhost:8000/api/v1"
      );
    } else {
      return (
        process.env.NEXT_PUBLIC_API_URL_SERVER ||
        "http://readum-backend:8000/api/v1"
      );
    }
  } else {
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
  }
}

/**
 * 現在の実行環境に基づいて適切なベースURLを選択
 */
export const BASE_URL =
  typeof window === "undefined"
    ? getBaseUrl("server") // サーバーサイドの場合
    : getBaseUrl("client"); // クライアントサイドの場合
