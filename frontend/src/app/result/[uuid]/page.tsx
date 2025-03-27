import Link from "next/link";
import { notFound } from "next/navigation";
import React from "react";

// 型定義
interface Option {
  A: string;
  B: string;
  C: string;
  D: string;
}

interface Question {
  content: string;
  options: Option;
  answer: string;
  explanation: string;
}

interface Quiz {
  questions: Question[];
}

interface UserAnswer {
  id: string;
  preview: Quiz;
  selected_options: string[];
}

async function fetchResult(uuid: string) {
  try {
    // APIエンドポイントからデータを取得
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_SIDE_URL}/result/${uuid}`
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
  const result: UserAnswer = await fetchResult(uuid);

  // 正答率を計算
  const calculateScore = () => {
    let correctCount = 0;
    const totalQuestions = result.preview.questions.length;

    result.preview.questions.forEach((question, index) => {
      if (result.selected_options[index] === question.answer) {
        correctCount++;
      }
    });

    return {
      correct: correctCount,
      total: totalQuestions,
      percentage: Math.round((correctCount / totalQuestions) * 100),
    };
  };

  const score = calculateScore();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">クイズ結果</h1>

      {/* 正答率の表示 */}
      <div
        className={`p-4 mb-6 rounded ${
          score.percentage === 100 ? "bg-green-100" : "bg-blue-100"
        }`}
      >
        <h2 className="font-bold text-lg">採点結果</h2>
        <p className="text-xl mt-2">
          {score.correct} / {score.total} 問正解 ({score.percentage}%)
        </p>
      </div>

      {/* クイズID */}
      <p className="mb-4">クイズID: {result.id}</p>

      {/* 問題と回答の表示 */}
      <div className="space-y-6">
        {result.preview.questions.map((question, qIndex) => (
          <div key={qIndex} className="border p-4 rounded shadow-sm">
            <h3 className="font-bold text-lg mb-2">問題 {qIndex + 1}</h3>
            <p className="mb-4">{question.content}</p>

            <div className="space-y-2 mb-4">
              <h4 className="font-medium">選択肢:</h4>
              {Object.entries(question.options).map(([key, value]) => (
                <div key={key} className="pl-4">
                  <label className="flex items-start space-x-2">
                    <input
                      type="radio"
                      name={`question-${qIndex}`}
                      value={key}
                      checked={result.selected_options[qIndex] === key}
                      readOnly
                      disabled
                      className="form-radio mt-1"
                    />
                    <div>
                      <span
                        className={`font-medium ${
                          key === question.answer
                            ? "text-green-600"
                            : result.selected_options[qIndex] === key &&
                              key !== question.answer
                            ? "text-red-600"
                            : ""
                        }`}
                      >
                        {key}:
                      </span>
                      <span className="ml-1">{value}</span>
                    </div>
                  </label>
                </div>
              ))}
            </div>

            {/* 正誤と解説 */}
            <div
              className={`mt-4 p-3 rounded ${
                result.selected_options[qIndex] === question.answer
                  ? "bg-green-100"
                  : "bg-red-100"
              }`}
            >
              <p className="font-medium">
                {result.selected_options[qIndex] === question.answer
                  ? "✅ 正解!"
                  : `❌ 不正解 (正解: ${question.answer})`}
              </p>
              <div className="mt-2">
                <h4 className="font-medium">解説:</h4>
                <p className="pl-4">{question.explanation}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* 戻るボタン */}
      <div className="mt-6">
        <Link
          href="/"
          className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded"
        >
          戻る
        </Link>
      </div>
    </div>
  );
}
