import Image from "next/image";
import React from "react";

interface Props {
  userAnswers: Record<number, string>;
  handleSubmitAnswer: () => Promise<void>;
  questionCount: number;
  isSubmitted: boolean;
}

export const SubmitButton: React.FC<Props> = ({
  userAnswers,
  handleSubmitAnswer,
  questionCount,
  isSubmitted,
}) => {
  return (
    <button
      onClick={handleSubmitAnswer}
      disabled={
        Object.keys(userAnswers).length !== questionCount || isSubmitted
      }
      className={`w-full bg-emerald-500 flex justify-center items-center text-white font-bold py-3 px-4 rounded-full disabled:opacity-50 duration-300 ${
        Object.keys(userAnswers).length !== questionCount
          ? "cursor-not-allowed"
          : `${
              isSubmitted
                ? "cursor-not-allowed"
                : "cursor-pointer hover:bg-emerald-600"
            }`
      }`}
    >
      <Image
        src="/icons/check.svg"
        alt="Check mark icon"
        width={24}
        height={24}
        className="mr-2"
      />
      {isSubmitted ? "回答の採点中です…" : "回答を送信する"}
    </button>
  );
};
