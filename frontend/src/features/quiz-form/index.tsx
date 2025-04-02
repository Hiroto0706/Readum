"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Description } from "@/features/quiz-form/components/description";
import { QuizResponse } from "@/features/quiz-form/types";
import { InputForm } from "@/features/quiz-form/components/input-form";
import { ErrorMessage } from "@/features/quiz-form/components/error-message";
import Image from "next/image";

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
      {!quizResponse && (
        <>
          <Description />

          <ErrorMessage error={error} />

          <InputForm
            setUserAnswers={setUserAnswers}
            setIsSubmitted={setIsSubmitted}
            setError={setError}
            setQuizResponse={setQuizResponse}
          />
        </>
      )}

      {quizResponse && (
        <div className="pt-8">
          <h2 className="text-xl font-bold flex items-center text-emerald-500 mb-6">
            <Image
              src="/icons/star.svg"
              alt="Star icon"
              width={20}
              height={20}
              className="mr-2"
            />
            クイズに回答しよう！
          </h2>

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

          <div className="space-y-6 mb-16">
            {quizResponse.preview.questions.map((question, qIndex) => (
              <div
                key={qIndex}
                className="rounded-xl shadow-md overflow-hidden"
              >
                <div className="font-bold text-lg text-white px-6 py-2 bg-emerald-500 flex items-center">
                  <span className="rounded-full bg-white text-emerald-500 w-8 h-8 block flex justify-center items-center mr-2">
                    {qIndex + 1}
                  </span>
                  {question.content}
                </div>

                <div className="space-y-2 p-6">
                  {Object.entries(question.options).map(([key, value]) => (
                    <div key={key}>
                      <label
                        className={`flex items-center space-x-2 border rounded-lg p-3 cursor-pointer ${
                          userAnswers[qIndex] === key
                            ? "bg-emerald-50 border-emerald-500"
                            : "border-gray-300 hover:bg-gray-100"
                        } duration-300`}
                      >
                        <input
                          type="radio"
                          name={`question-${qIndex}`}
                          value={key}
                          checked={userAnswers[qIndex] === key}
                          onChange={() => handleAnswerSelect(qIndex, key)}
                          disabled={isSubmitted}
                          className="appearance-none w-6 h-6 border border-emerald-500 rounded-full checked:border-emerald-500 transition-colors"
                        />
                        {userAnswers[qIndex] === key && (
                          // ml-1は丸を縦横中央に配置するため
                          <div className="absolute w-4 h-4 ml-1 bg-emerald-500 rounded-full pointer-events-none"></div>
                        )}
                        <span className="ml-2">{value}</span>
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

          <div className="mb-16">
            <div className="w-full bg-gray-100 rounded-full h-6 overflow-hidden mb-6">
              <div
                className="bg-emerald-500 h-6 rounded-l-full transition-all duration-500 ease-out"
                style={{
                  width: `${
                    (Object.keys(userAnswers).length /
                      quizResponse.preview.questions.length) *
                    100
                  }%`,
                }}
              ></div>
            </div>

            <div className="flex justify-between mb-2 font-bold">
              <span className="text-sm">
                {Object.keys(userAnswers).length} of{" "}
                {quizResponse.preview.questions.length} questions answered
              </span>
              <span className="text-sm font-medium text-emerald-600 font-bold">
                {Math.round(
                  (Object.keys(userAnswers).length /
                    quizResponse.preview.questions.length) *
                    100
                )}
                %
              </span>
            </div>
          </div>

          <div>
            {!isSubmitted ? (
              <button
                onClick={handleGradeQuiz}
                disabled={
                  Object.keys(userAnswers).length !==
                  quizResponse.preview.questions.length
                }
                className={`w-full bg-emerald-500 flex justify-center items-center text-white font-bold py-3 px-4 rounded-full disabled:opacity-50 duration-300 ${
                  Object.keys(userAnswers).length !==
                  quizResponse.preview.questions.length
                    ? "cursor-not-allowed"
                    : "cursor-pointer hover:bg-emerald-600"
                }`}
              >
                <Image
                  src="/icons/check.svg"
                  alt="Check mark icon"
                  width={24}
                  height={24}
                  className="mr-2"
                />
                回答を送信する
              </button>
            ) : (
              <button
                onClick={() => {
                  setUserAnswers({});
                  setIsSubmitted(false);
                }}
                className={`w-full bg-blue-500 flex justify-center items-center text-white font-bold py-3 px-4 rounded-full disabled:opacity-50 duration-300 ${
                  Object.keys(userAnswers).length !==
                  quizResponse.preview.questions.length
                    ? "cursor-not-allowed"
                    : "cursor-pointer hover:bg-blue-600"
                }`}
              >
                もう一度解く
              </button>
            )}
          </div>
        </div>
      )}
    </>
  );
};
