"use client";

import React, { useState } from "react";
import { QuizResponse } from "@/features/quiz-form/types";
import Image from "next/image";
import { TextArea } from "@/features/quiz-form/components/input-form/components/textarea";
import { DifficultyLevel } from "@/features/quiz-form/components/input-form/components/difficulty-level";
import { QuestionCount } from "@/features/quiz-form/components/input-form/components/question-count";
import { SubmitButton } from "@/features/quiz-form/components/input-form/components/submit-button";
import {
  Difficulty,
  QuizType,
} from "@/features/quiz-form/components/input-form/types";
import { BASE_URL } from "@/utils";

interface Props {
  setUserAnswers: React.Dispatch<React.SetStateAction<Record<number, string>>>;
  setIsSubmitted: React.Dispatch<React.SetStateAction<boolean>>;
  setError: React.Dispatch<React.SetStateAction<string>>;
  setQuizResponse: React.Dispatch<React.SetStateAction<QuizResponse | null>>;
}

export const InputForm: React.FC<Props> = ({
  setUserAnswers,
  setIsSubmitted,
  setError,
  setQuizResponse,
}) => {
  const [quizType, setQuizType] = useState<QuizType>(QuizType.TEXT);
  const [content, setContent] = useState("");
  const [difficulty, setDifficulty] = useState<Difficulty>(
    Difficulty.INTERMEDIATE
  );
  const [questionCount, setQuestionCount] = useState<number | null>(5);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    setQuizResponse(null);
    setUserAnswers({});
    setIsSubmitted(false);

    if (!questionCount) {
      return;
    }
    if (questionCount < 3 || questionCount > 20) {
      setError("問題数は3〜20問の間で設定してください");
      setIsSubmitting(false);
      return;
    }

    if (quizType === QuizType.URL) {
      try {
        const url = new URL(content);
        if (!url.protocol.startsWith("http")) {
          setError("URLはhttp://またはhttps://で始まる必要があります");
          setIsSubmitting(false);
          return;
        }
      } catch (error) {
        console.error("URL検証エラー:", error);
        setError("有効なURLを入力してください");
        setIsSubmitting(false);
        return;
      }
    }

    try {
      const response = await fetch(BASE_URL + "/quiz/create_quiz", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          type: quizType,
          content,
          difficulty,
          questionCount,
        }),
      });

      if (!response.ok) {
        throw new Error("クイズの作成に失敗しました");
      }

      const data = await response.json();
      setQuizResponse(data);
    } catch (error) {
      console.error("Error:", error);
      setError("クイズの作成中にエラーが発生しました");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="shadow-xl rounded-2xl mb-32 truncate mx-2 md:mx-0">
      <div className="flex justify-center py-3 text-center font-bold text-lg text-white bg-emerald-500">
        <Image
          src="/icons/generate.svg"
          alt="Generate icon"
          width={20}
          height={20}
          className="mr-2"
        />
        <p>自分だけのクイズを作る</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 p-4 md:p-8">
        <TextArea
          setQuizType={setQuizType}
          isSubmitting={isSubmitting}
          quizType={quizType}
          content={content}
          setContent={setContent}
        />

        <DifficultyLevel
          difficulty={difficulty}
          setDifficulty={setDifficulty}
          isSubmitting={isSubmitting}
        />

        <QuestionCount
          questionCount={questionCount}
          setQuestionCount={setQuestionCount}
          isSubmitting={isSubmitting}
        />

        <SubmitButton isSubmitting={isSubmitting} />
      </form>
    </div>
  );
};
