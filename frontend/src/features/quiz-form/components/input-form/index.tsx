"use client";

import React, { useState } from "react";
import { QuizResponse } from "../../types";
import Image from "next/image";

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
  const [difficulty, setDifficulty] = useState("intermediate");
  const [questionCount, setQuestionCount] = useState(5);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    setQuizResponse(null);
    setUserAnswers({});
    setIsSubmitted(false);

    // 問題数のバリデーションを追加
    if (questionCount < 3 || questionCount > 20) {
      setError("問題数は3〜20問の間で設定してください");
      setIsSubmitting(false);
      return;
    }

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
    <div className="shadow-xl rounded-2xl mb-16 truncate mx-2 md:mx-0">
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
        <div className="flex rounded-md space-x-1 overflow-hidden p-1 bg-emerald-50 font-bold">
          <button
            type="button"
            onClick={() => setQuizType("text")}
            disabled={isSubmitting}
            className={`flex-1 py-2 px-4 flex justify-center items-center rounded-md duration-300 ${
              quizType === "text" ? "bg-emerald-500 text-white" : ""
            } ${isSubmitting ? "cursor-not-allowed" : "cursor-pointer"}`}
          >
            <Image
              src={`/icons/text${quizType === "text" ? "-active" : ""}.svg`}
              alt="Generate icon"
              width={20}
              height={20}
              className="mr-1"
            />
            <p>テキスト</p>
          </button>
          <button
            type="button"
            onClick={() => setQuizType("url")}
            disabled={isSubmitting}
            className={`flex-1 py-2 px-4 flex justify-center items-center rounded-md duration-300 ${
              quizType === "url" ? "bg-emerald-500 text-white" : ""
            } ${isSubmitting ? "cursor-not-allowed" : "cursor-pointer"}`}
          >
            <Image
              src={`/icons/web${quizType === "url" ? "-active" : ""}.svg`}
              alt="Generate icon"
              width={20}
              height={20}
              className="mr-1"
            />
            <p>URL</p>
          </button>
        </div>

        <div>
          {quizType === "text" ? (
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full p-2 border border-emerald-300 rounded"
              rows={5}
              disabled={isSubmitting}
              placeholder="読書メモをここに入力してください"
              required
            />
          ) : (
            <input
              type="url"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full p-2 border border-emerald-300 rounded"
              disabled={isSubmitting}
              placeholder="https://example.com"
              pattern="https?://.*"
              required
            />
          )}
        </div>

        <div>
          <label className="flex justify-start mb-2 font-medium">
            <span className="mr-1">⚡️</span>
            <p className="font-bold">難易度</p>
          </label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="w-full p-2 border border-emerald-300 rounded"
            required
            disabled={isSubmitting}
          >
            <option value="beginner">
              初級 <span>📚</span>
            </option>
            <option value="intermediate">
              中級 <span>🧠</span>
            </option>
            <option value="advanced">
              上級 <span>🚀</span>
            </option>
          </select>
        </div>

        <div>
          <label className="flex justify-start mb-2 font-medium">
            <span className="mr-1">💡</span>
            <p className="font-bold">問題数</p>
          </label>
          <input
            type="number"
            min="3"
            max="20"
            value={questionCount}
            onChange={(e) => setQuestionCount(parseInt(e.target.value))}
            className="w-full p-2 border border-emerald-300 rounded"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            3〜20問の間で設定してください
          </p>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full flex justify-center bg-emerald-500 text-white font-medium py-2 px-4 rounded disabled:opacity-50 duration-300 ${
            isSubmitting
              ? "cursor-not-allowed"
              : "hover:bg-emerald-600 cursor-pointer"
          }`}
        >
          <Image
            src="/icons/generate.svg"
            alt="Generate icon"
            width={20}
            height={20}
            className="mr-2"
          />
          <p>{isSubmitting ? "作成中..." : "クイズを作成する！"}</p>
        </button>
      </form>
    </div>
  );
};
