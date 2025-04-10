"use server";

import { BASE_URL } from "@/config";
import {
  Difficulty,
  QuizType,
} from "@/features/quiz-form/components/input-form/types";
import { QuizResponse } from "@/features/quiz-form/types";

export async function createQuiz(formData: {
  quizType: QuizType;
  content: string;
  difficulty: Difficulty;
  questionCount: number;
}): Promise<{ data?: QuizResponse }> {
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
      throw new Error("クイズの作成に失敗しました");
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    console.error("Error:", error);
    throw new Error("クイズの作成中にエラーが発生しました");
  }
}
