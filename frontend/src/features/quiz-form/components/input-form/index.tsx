"use client";

import React, { useState } from "react";
import { QuizResponse } from "../../types";

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
  const [quizType, setQuizType] = useState("text");
  const [content, setContent] = useState("");
  const [difficulty, setDifficulty] = useState("beginner");
  const [questionCount, setQuestionCount] = useState(5);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    setQuizResponse(null);
    setUserAnswers({});
    setIsSubmitted(false);

    // URLの検証（quizTypeがurlの場合）
    if (quizType === "url") {
      try {
        const url = new URL(content);
        if (!url.protocol.startsWith("http")) {
          setError("URLはhttp://またはhttps://で始まる必要があります");
          setIsSubmitting(false);
          return;
        }
      } catch (e) {
        setError("有効なURLを入力してください");
        setIsSubmitting(false);
        return;
      }
    }

    try {
      // Server Actionの呼び出し
      const response = await fetch(
        process.env.NEXT_PUBLIC_API_URL + "/quiz/create_quiz",
        {
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
        }
      );

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
    <div className="mb-16 shadow-xl rounded-2xl mb-16 truncate">
      <p className="py-3 text-center font-bold text-lg text-white bg-emerald-500">
        自分だけのクイズを作る
      </p>

      <form onSubmit={handleSubmit} className="space-y-6 p-8">
        <div>
          <label className="block mb-2 font-medium">クイズのタイプ</label>
          <select
            value={quizType}
            onChange={(e) => setQuizType(e.target.value)}
            className="w-full p-2 border rounded"
            required
          >
            <option value="text">テキスト</option>
            <option value="url">URL</option>
          </select>
        </div>

        <div>
          <label className="block mb-2 font-medium">
            {quizType === "text" ? "テキスト内容" : "URL"}
          </label>
          {quizType === "text" ? (
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full p-2 border rounded"
              rows={5}
              required
            />
          ) : (
            <input
              type="url"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="https://example.com"
              pattern="https?://.*"
              required
            />
          )}
        </div>

        <div>
          <label className="block mb-2 font-medium">難易度</label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="w-full p-2 border rounded"
            required
          >
            <option value="beginner">初級📚</option>
            <option value="intermediate">中級🧠</option>
            <option value="advanced">上級🚀</option>
          </select>
        </div>

        <div>
          <label className="block mb-2 font-medium">問題数</label>
          <input
            type="number"
            min="3"
            max="20"
            value={questionCount}
            onChange={(e) => setQuestionCount(parseInt(e.target.value))}
            className="w-full p-2 border rounded"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            3〜20問の間で設定してください
          </p>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded disabled:opacity-50"
        >
          {isSubmitting ? "作成中..." : "クイズを作成"}
        </button>
      </form>
    </div>
  );
};
