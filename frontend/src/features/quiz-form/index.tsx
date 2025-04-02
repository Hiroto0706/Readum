"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Description } from "@/features/quiz-form/components/description";
import { QuizResponse } from "@/features/quiz-form/types";
import { InputForm } from "@/features/quiz-form/components/input-form";
import { ErrorMessage } from "@/features/quiz-form/components/error-message";

export const QuizForm: React.FC = () => {
  const [error, setError] = useState("");
  const [quizResponse, setQuizResponse] = useState<QuizResponse | null>(null);

  // 回答と採点結果の状態
  const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [score, setScore] = useState<{ correct: number; total: number }>({
    correct: 0,
    total: 0,
  });

  const router = useRouter();

  // 回答を選択したときのハンドラ
  const handleAnswerSelect = (questionIndex: number, answer: string) => {
    setUserAnswers((prev) => ({
      ...prev,
      [questionIndex]: answer,
    }));
  };

  // 採点処理
  const handleGradeQuiz = async () => {
    if (!quizResponse) return;

    let correctCount = 0;
    const totalQuestions = quizResponse.preview.questions.length;

    quizResponse.preview.questions.forEach((question, index) => {
      if (userAnswers[index] === question.answer) {
        correctCount++;
      }
    });

    setScore({
      correct: correctCount,
      total: totalQuestions,
    });

    setIsSubmitted(true);

    // バックエンドにユーザーの回答を送信
    try {
      // UserAnswer形式のデータを作成
      const selectedOptions = Object.keys(userAnswers)
        .sort((a, b) => parseInt(a) - parseInt(b))
        .map((key) => userAnswers[parseInt(key)]);

      const submissionData = {
        id: quizResponse.id,
        preview: quizResponse.preview,
        selected_options: selectedOptions,
      };

      // APIを呼び出し
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/quiz/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(submissionData),
      });

      console.log("回答が正常に送信されました");
    } catch (error) {
      console.error("回答の送信中にエラーが発生しました:", error);
      // ユーザー体験を損なわないため、エラーが発生しても採点結果は表示する
      // 必要に応じてここでエラー通知を表示することも可能
      alert("回答の送信中にエラーが発生しました");
    }
  };

  return (
    <>
      <Description />

      <ErrorMessage error={error} />

      {!quizResponse && (
        <>
          <InputForm
            setUserAnswers={setUserAnswers}
            setIsSubmitted={setIsSubmitted}
            setError={setError}
            setQuizResponse={setQuizResponse}
          />
        </>
      )}

      {quizResponse && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">作成されたクイズ</h2>
          <p className="mb-4">クイズID: {quizResponse.id}</p>

          {isSubmitted && (
            <div
              className={`p-4 mb-6 rounded ${
                score.correct === score.total ? "bg-green-100" : "bg-blue-100"
              }`}
            >
              <h3 className="font-bold text-lg">採点結果</h3>
              <p className="text-xl mt-2">
                {score.correct} / {score.total} 問正解 (
                {Math.round((score.correct / score.total) * 100)}%)
              </p>
            </div>
          )}

          <div className="space-y-6">
            {quizResponse.preview.questions.map((question, qIndex) => (
              <div key={qIndex} className="border p-4 rounded shadow-sm">
                <h3 className="font-bold text-lg mb-2">問題 {qIndex + 1}</h3>
                <p className="mb-4">{question.content}</p>

                <div className="space-y-2 mb-4">
                  <h4 className="font-medium">選択肢:</h4>
                  {Object.entries(question.options).map(([key, value]) => (
                    <div key={key} className="pl-4">
                      <label className="flex items-center space-x-2">
                        <input
                          type="radio"
                          name={`question-${qIndex}`}
                          value={key}
                          checked={userAnswers[qIndex] === key}
                          onChange={() => handleAnswerSelect(qIndex, key)}
                          disabled={isSubmitted}
                          className="form-radio"
                        />
                        <span
                          className={`font-medium ${
                            isSubmitted && key === question.answer
                              ? "text-green-600"
                              : ""
                          }`}
                        >
                          {key}:
                        </span>
                        <span>{value}</span>
                      </label>
                    </div>
                  ))}
                </div>

                {isSubmitted && (
                  <div
                    className={`mt-4 p-3 rounded ${
                      userAnswers[qIndex] === question.answer
                        ? "bg-green-100"
                        : "bg-red-100"
                    }`}
                  >
                    <p className="font-medium">
                      {userAnswers[qIndex] === question.answer
                        ? "✅ 正解!"
                        : `❌ 不正解 (正解: ${question.answer})`}
                    </p>
                    <div className="mt-2">
                      <h4 className="font-medium">解説:</h4>
                      <p className="pl-4">{question.explanation}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-6 flex space-x-4">
            {!isSubmitted ? (
              <button
                onClick={handleGradeQuiz}
                disabled={
                  Object.keys(userAnswers).length !==
                  quizResponse.preview.questions.length
                }
                className="bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded disabled:opacity-50"
              >
                回答を送信して採点する
              </button>
            ) : (
              <button
                onClick={() => {
                  setUserAnswers({});
                  setIsSubmitted(false);
                }}
                className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded"
              >
                もう一度解く
              </button>
            )}

            <button
              onClick={() => router.push(`/quiz/${quizResponse.id}`)}
              className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded"
            >
              クイズを共有する
            </button>
          </div>
        </div>
      )}
    </>
  );
};
