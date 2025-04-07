"use client";

import ShareButton from "@/components/share-link";
import React, { useEffect, useState } from "react";
import { ResultCard } from "@/features/result/components/result-card";
import Link from "next/link";
import {
  DifficultyMessage,
  ResultMessage,
  Score,
  UserAnswer,
} from "@/features/result/types";
import { TopMessage } from "@/features/result/components/top-message";
import Image from "next/image";
import { calculateScore, getResultMessage } from "./utils";

interface Props {
  result: UserAnswer;
}

export const Result: React.FC<Props> = ({ result }) => {
  const [animatedPercentage, setAnimatedPercentage] = useState(0);

  const score: Score = calculateScore(result);

  const difficultyKey = result.difficultyValue
    ? (result.difficultyValue as keyof typeof DifficultyMessage)
    : "intermediate";
  const { value: difficultyValue, style: difficultyStyle } =
    DifficultyMessage[difficultyKey];

  const resultMessage = getResultMessage(score.percentage);

  // アニメーション効果
  useEffect(() => {
    const duration = 1000;
    const interval = 30;
    const steps = duration / interval;
    const increment = score.percentage / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= score.percentage) {
        setAnimatedPercentage(score.percentage);
        clearInterval(timer);
      } else {
        setAnimatedPercentage(Math.round(current));
      }
    }, interval);

    return () => clearInterval(timer);
  }, [score.percentage]);

  return (
    <div className="container mx-auto px-2 md:px-4 py-6">
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

      <TopMessage
        resultMessage={resultMessage}
        difficultyValue={difficultyValue}
        difficultyStyle={difficultyStyle}
        percentage={animatedPercentage}
        score={score}
      />

      <ShareButton />

      <div className="space-y-6">
        {result.preview.questions.map((question, qIndex) => (
          <ResultCard
            key={qIndex}
            qIndex={qIndex}
            options={question.options}
            question={question.content}
            answer={question.answer}
            explanation={question.explanation}
            selectedOptions={result.selectedOptions}
          />
        ))}
      </div>

      <div className="mt-6 flex justify-end">
        <Link
          href="/"
          className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded"
        >
          TOP
        </Link>
      </div>
    </div>
  );
};
