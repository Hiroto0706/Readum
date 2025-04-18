"use client";

import Image from "next/image";
import React from "react";
import { QuizType } from "@/features/quiz-form/components/input-form/types";

interface Props {
  isSubmitting: boolean;
  quizType: QuizType;
  setQuizType: React.Dispatch<React.SetStateAction<QuizType>>;
  content: string;
  setContent: (value: React.SetStateAction<string>) => void;
}

const DISABLED_CRAWL =
  process.env.DISABLED_CRAWL !== "false" ? true : false;

export const TextArea: React.FC<Props> = ({
  setQuizType,
  isSubmitting,
  quizType,
  content,
  setContent,
}) => {
  return (
    <>
      <div className="flex rounded-md space-x-1 overflow-hidden p-1 bg-emerald-50 font-bold">
        <button
          type="button"
          onClick={() => setQuizType(QuizType.TEXT)}
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
          onClick={() => setQuizType(QuizType.URL)}
          disabled={isSubmitting || DISABLED_CRAWL}
          className={`flex-1 py-2 px-4 flex justify-center items-center rounded-md duration-300 ${
            quizType === "url" ? "bg-emerald-500 text-white" : ""
          } ${
            isSubmitting || DISABLED_CRAWL
              ? "cursor-not-allowed"
              : "cursor-pointer"
          }`}
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
        {quizType === QuizType.TEXT ? (
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className={`w-full h-64 p-2 border border-emerald-300 rounded ${
              isSubmitting ? "cursor-not-allowed" : ""
            }`}
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
            className={`w-full p-2 border border-emerald-300 rounded ${
              isSubmitting ? "cursor-not-allowed" : ""
            }`}
            disabled={isSubmitting}
            placeholder="https://example.com"
            pattern="https?://.*"
            required
          />
        )}
      </div>
    </>
  );
};
