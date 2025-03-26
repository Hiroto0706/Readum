import { notFound } from "next/navigation";
import React from "react";

async function fetchResult(uuid: string) {
  try {
    // APIエンドポイントからデータを取得
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_SIDE_URL}/result/${uuid}`,
      {
        cache: "no-store", // SSRで毎回最新データを取得
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        return notFound();
      }
      throw new Error(`Failed to fetch result: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching result:", error);
    throw error;
  }
}

interface Props {
  params: Promise<{ uuid: string }>;
}

export default async function Page({ params }: Props) {
  const { uuid } = await params;
  const result = await fetchResult(uuid);

  console.log(result);
  console.log(result.preview);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">テスト結果</h1>

      <div className="bg-white shadow-md rounded p-6">
        <h2 className="text-xl font-semibold mb-2">{result.preview.title}</h2>

        <div className="mt-4">
          <h3 className="text-lg font-medium mb-2">回答内容:</h3>
          <ul className="space-y-4">
            {result.preview.questions.map((question: any, index: number) => (
              <li key={index} className="border-b pb-3">
                <p className="font-medium">
                  {index + 1}. {question.text}
                </p>
                <div className="mt-2">
                  <p className="text-sm text-gray-600">
                    あなたの回答: {result.selected_options[index]}
                  </p>
                  {/* 正解を表示する場合はここに追加 */}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
