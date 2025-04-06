import Image from "next/image";
import React from "react";
import { Score } from "@/features/result/types";

interface Props {
  resultMessage: string;
  difficultyValue: string;
  difficultyStyle: string;
  animatedPercentage: number;
  score: Score;
}

export const TopMessage: React.FC<Props> = ({
  resultMessage,
  difficultyValue,
  difficultyStyle,
  animatedPercentage,
  score,
}) => {
  return (
    <>
      <h1 className="text-2xl font-bold mb-4 flex items-center">
        <Image
          src="/icons/star.svg"
          alt="Generate icon"
          width={28}
          height={28}
          className="mr-2"
        />
        クイズ結果
      </h1>

      <div className="rounded-lg text-center mb-8 shadow">
        <div className="w-full bg-emerald-500 rounded-t-lg text-white font-bold text-lg md:text-xl py-4 px-2 break-words">
          {resultMessage}
        </div>
        <div className="p-6 flex flex-col justify-center items-center">
          {difficultyValue && (
            <>
              <div className="mb-6 font-bold">
                <span
                  className={`py-2 px-4 rounded-full text-white ${difficultyStyle}`}
                >
                  {difficultyValue}
                </span>
              </div>
            </>
          )}
          <div className="w-36 h-36 bg-emerald-100 rounded-full flex justify-center items-center">
            <p className="font-bold text-4xl text-white w-28 h-28 rounded-full bg-emerald-500 flex justify-center items-center">
              {animatedPercentage}%
            </p>
          </div>
          <p className="mt-6 space-x-2 flex justify-center items-center">
            <span className="text-3xl font-bold text-emerald-500">
              {score.correct} / {score.total}
            </span>
            <span className="font-bold">correct</span>
          </p>
        </div>
      </div>
    </>
  );
};
