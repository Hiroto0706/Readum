"use server";

import { BASE_URL } from "@/config";
import {
  Difficulty,
  QuizType,
} from "@/features/quiz-form/components/input-form/types";
import { ErrorResponse, QuizResponse } from "@/features/quiz-form/types";

export async function createQuiz(formData: {
  quizType: QuizType;
  content: string;
  difficulty: Difficulty;
  questionCount: number;
}): Promise<{ data?: QuizResponse; error?: ErrorResponse }> {
  try {
    const response = await fetch(`${BASE_URL}/quiz/create_quiz`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: formData.quizType,
        content: formData.content,
        difficulty: formData.difficulty,
        questionCount: formData.questionCount,
      }),
    });

    if (!response.ok) {
      const statusCode = response.status;

      let errorMessage = "クイズの作成に失敗しました";

      // ステータスコードに基づいてメッセージをカスタマイズ
      if (statusCode === 400) {
        errorMessage =
          "入力内容に問題があります。テキストが短すぎるか、URLが無効です。";
      } else if (statusCode >= 500) {
        errorMessage =
          "サーバーでエラーが発生しました。しばらく経ってからもう一度お試しください。";
      }

      return {
        error: {
          status: statusCode,
          message: errorMessage,
        },
      };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    console.error("Error:", error);
    throw new Error("クイズの作成中にエラーが発生しました");
  }
}
