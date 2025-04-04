"use client";

import React from "react";

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
        min={process.env.NEXT_PUBLIC_MIN_QUESTION_COUNT}
        max={process.env.NEXT_PUBLIC_MAX_QUESTION_COUNT}
        value={questionCount ? questionCount : ""}
        onChange={(e) => setQuestionCount(parseInt(e.target.value))}
        className={`w-full p-2 border border-emerald-300 rounded ${
          isSubmitting ? "cursor-not-allowed" : ""
        }`}
        disabled={isSubmitting}
        required
      />
      <p className="text-sm text-gray-500 mt-1">
        {process.env.NEXT_PUBLIC_MIN_QUESTION_COUNT}〜
        {process.env.NEXT_PUBLIC_MAX_QUESTION_COUNT}
        問の間で設定してください
      </p>
    </div>
  );
};
