"use client";

import React from "react";

const MIN_QUESTION_COUNT = parseInt(
  process.env.NEXT_PUBLIC_MIN_QUESTION_COUNT || "3"
);
const MAX_QUESTION_COUNT = parseInt(
  process.env.NEXT_PUBLIC_MAX_QUESTION_COUNT || "10"
);

interface Props {
  questionCount: number | null;
  setQuestionCount: (value: React.SetStateAction<number | null>) => void;
  isSubmitting: boolean;
}

export const QuestionCount: React.FC<Props> = ({
  questionCount,
  setQuestionCount,
  isSubmitting,
}) => {
  return (
    <div>
      <label className="flex justify-start mb-2 font-medium">
        <span className="mr-1">💡</span>
        <p className="font-bold">問題数</p>
      </label>
      <input
        type="number"
        min={MIN_QUESTION_COUNT}
        max={MAX_QUESTION_COUNT}
        value={questionCount ? questionCount : ""}
        onChange={(e) => setQuestionCount(parseInt(e.target.value))}
        className={`w-full p-2 border border-emerald-300 rounded ${
          isSubmitting ? "cursor-not-allowed" : ""
        }`}
        disabled={isSubmitting}
        required
      />
      <div>
        <button
          type="button"
          onClick={() => setQuestionCount(3)}
          className={`font-bold bg-emerald-500 text-white rounded-full my-3 py-1 px-3 w-[calc(33%-8px)] box-border text-xs md:text-base duration-300 mr-2 ${
            isSubmitting
              ? "cursor-not-allowed"
              : "cursor-pointer hover:bg-emerald-600"
          }`}
          disabled={isSubmitting}
        >
          3問
        </button>
        <button
          type="button"
          onClick={() => setQuestionCount(5)}
          className={`font-bold bg-emerald-500 text-white rounded-full my-3 py-1 px-3 w-[calc(33%-8px)] box-border text-xs md:text-base duration-300 mx-2 ${
            isSubmitting
              ? "cursor-not-allowed"
              : "cursor-pointer hover:bg-emerald-600"
          }`}
          disabled={isSubmitting}
        >
          5問
        </button>
        <button
          type="button"
          onClick={() => setQuestionCount(10)}
          className={`font-bold bg-emerald-500 text-white rounded-full my-3 py-1 px-3 w-[calc(33%-8px)] box-border text-xs md:text-base duration-300 ml-2 ${
            isSubmitting
              ? "cursor-not-allowed"
              : "cursor-pointer hover:bg-emerald-600"
          }`}
          disabled={isSubmitting}
        >
          10問
        </button>
      </div>
      <p className="text-sm text-gray-500 mt-1">
        {MIN_QUESTION_COUNT}〜{MAX_QUESTION_COUNT}問の間で設定してください
      </p>
    </div>
  );
};
