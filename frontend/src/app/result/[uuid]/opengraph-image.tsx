import { DifficultyMessage, Score, UserAnswer } from "@/features/result/types";
import { calculateScore, getResultMessage } from "@/features/result/utils";
import { ImageResponse } from "next/og";
import { cache } from "react";

export const runtime = "edge";

export const alt = "Readum｜クイズ結果";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

// 結果データを取得する関数
const fetchResult = cache(async (uuid: string): Promise<UserAnswer | null> => {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_SIDE_URL}/result/${uuid}`
    );

    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error("Failed to fetch result data:", error);
    return null;
  }
});

interface Props {
  params: Promise<{ uuid: string }>;
}

export default async function Image({ params }: Props) {
  const uuid = (await params).uuid;
  const result = await fetchResult(uuid);

  if (!result) {
    return new ImageResponse(
      (
        <div
          style={{
            width: "100%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "white",
            padding: "20px",
            fontFamily: "sans-serif",
          }}
        >
          <div
            style={{
              fontSize: "32px",
              fontWeight: "bold",
              marginBottom: "16px",
              display: "flex",
              justifyContent: "center",
            }}
          >
            データが見つかりません
          </div>
          <div
            style={{
              fontSize: "24px",
              display: "flex",
              justifyContent: "center",
            }}
          >
            このクイズ結果は存在しないか、削除された可能性があります。
          </div>
        </div>
      ),
      {
        ...size,
      }
    );
  }

  // スコアを計算
  const score: Score = calculateScore(result);

  // 結果メッセージを取得
  const resultMessage = getResultMessage(score.percentage);

  // 難易度スタイルを取得
  const difficultyKey =
    (result.difficultyValue as keyof typeof DifficultyMessage) ||
    "intermediate";
  const difficultyInfo =
    DifficultyMessage[difficultyKey] || DifficultyMessage.intermediate;
  const difficultyValue = difficultyInfo.value;
  const difficultyStyle = difficultyInfo.style;

  // Tailwindクラス名からCSSの色に変換
  let bgColor = "#14b8a6"; // デフォルト teal-500
  if (difficultyStyle === "bg-amber-500") bgColor = "#f59e0b";
  if (difficultyStyle === "bg-teal-500") bgColor = "#14b8a6";
  if (difficultyStyle === "bg-violet-500") bgColor = "#8b5cf6";

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          backgroundColor: "white",
          margin: "0",
          padding: "0",
          fontFamily: "sans-serif",
          overflow: "hidden",
        }}
      >
        {/* ヘッダー部分 */}
        <div
          style={{
            width: "100%",
            backgroundColor: "#10b981", // bg-emerald-500
            color: "white",
            fontWeight: "bold",
            fontSize: "40px",
            padding: "30px 20px",
            textAlign: "center",
            wordBreak: "break-word",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {resultMessage}
        </div>

        {/* コンテンツ部分 */}
        <div
          style={{
            width: "100%",
            flex: "1",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "white",
            padding: "30px 20px",
          }}
        >
          {/* 難易度バッジ */}
          {difficultyValue && (
            <div
              style={{
                marginBottom: "30px",
                fontWeight: "bold",
                display: "flex",
                justifyContent: "center",
              }}
            >
              <span
                style={{
                  padding: "12px 30px",
                  borderRadius: "9999px",
                  backgroundColor: bgColor,
                  color: "white",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  fontSize: "32px",
                }}
              >
                {difficultyValue}
              </span>
            </div>
          )}

          {/* パーセンテージの円 */}
          <div
            style={{
              width: "240px",
              height: "240px",
              backgroundColor: "#d1fae5", // bg-emerald-100
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              margin: "0 auto 40px auto",
            }}
          >
            <div
              style={{
                fontWeight: "bold",
                fontSize: "70px",
                color: "white",
                width: "190px",
                height: "190px",
                borderRadius: "50%",
                backgroundColor: "#10b981", // bg-emerald-500
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              {score.percentage}%
            </div>
          </div>

          {/* スコア表示 */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <div
              style={{
                fontSize: "50px",
                fontWeight: "bold",
                color: "#10b981", // text-emerald-500
                display: "flex",
                alignItems: "center",
                marginRight: "15px",
              }}
            >
              {score.correct} / {score.total}
            </div>
            <div
              style={{
                fontWeight: "bold",
                display: "flex",
                alignItems: "center",
                fontSize: "36px",
              }}
            >
              correct
            </div>
          </div>
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
