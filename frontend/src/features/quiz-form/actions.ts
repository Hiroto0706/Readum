"use server";

import { BASE_URL } from "@/utils";
import { Quiz } from "@/features/quiz-form/types";

export async function submitQuiz(formData: {
  id: string;
  preview: Quiz;
  selectedOptions: string[];
  difficultyValue: string;
}): Promise<{ uuid?: string }> {
  try {
    const response = await fetch(`${BASE_URL}/quiz/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      throw new Error("APIからのレスポンスが正常ではありません");
    }

    const data = await response.json();
    return { uuid: data.uuid };
  } catch (error) {
    console.error("回答の送信中にエラーが発生しました:", error);
    throw new Error("回答の送信中にエラーが発生しました");
  }
}
