"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Description } from "@/features/quiz-form/components/description";
import { QuizResponse } from "@/features/quiz-form/types";
import { InputForm } from "@/features/quiz-form/components/input-form";
import { ErrorMessage } from "@/features/quiz-form/components/error-message";
import { QuizList } from "@/features/quiz-form/components/quiz-list";
import { submitQuiz } from "@/features/quiz-form/actions";

export const QuizForm: React.FC = () => {
  const [error, setError] = useState("");
  const [quizResponse, setQuizResponse] = useState<QuizResponse | null>(null);
  // 回答と採点結果の状態
  const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  const router = useRouter();

  // 回答を選択したときのハンドラ
  const handleAnswerSelect = (questionIndex: number, answer: string) => {
    setUserAnswers((prev) => ({
      ...prev,
      [questionIndex]: answer,
    }));
  };

  const handleSubmitAnswer = async () => {
    if (!quizResponse) return;

    setIsSubmitted(true);

    try {
      // UserAnswer形式のデータを作成
      const selectedOptions = Object.keys(userAnswers)
        .sort((a, b) => parseInt(a) - parseInt(b))
        .map((key) => userAnswers[parseInt(key)]);

      const submissionData = {
        id: quizResponse.id,
        preview: quizResponse.preview,
        selectedOptions: selectedOptions,
        difficultyValue: quizResponse.difficultyValue,
      };

      const result = await submitQuiz(submissionData);

      if (result.uuid) {
        router.push(`/result/${result.uuid}`);
      } else {
        throw new Error("APIからのレスポンスが正常ではありません");
      }
    } catch (error) {
      console.error("回答の送信中にエラーが発生しました:", error);
      setError("回答の送信中にエラーが発生しました");
      setIsSubmitted(false);
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
        <QuizList
          quizResponse={quizResponse}
          userAnswers={userAnswers}
          handleAnswerSelect={handleAnswerSelect}
          handleSubmitAnswer={handleSubmitAnswer}
          isSubmitted={isSubmitted}
          error={error}
        />
      )}
    </>
  );
};
