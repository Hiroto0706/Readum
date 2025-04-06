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

interface Props {
  result: UserAnswer;
}

export const Result: React.FC<Props> = ({ result }) => {
  const [animatedPercentage, setAnimatedPercentage] = useState(0);

  const calculateScore = (): Score => {
    let correctCount = 0;
    const totalQuestions = result.preview.questions.length;

    result.preview.questions.forEach((question, index) => {
      if (result.selectedOptions[index] === question.answer) {
        correctCount++;
      }
    });

    return {
      correct: correctCount,
      total: totalQuestions,
      percentage: Math.round((correctCount / totalQuestions) * 100),
    };
  };

  const score: Score = calculateScore();

  const difficultyKey = result.difficultyValue
    ? (result.difficultyValue as keyof typeof DifficultyMessage)
    : "intermediate";
  const { value: difficultyValue, style: difficultyStyle } =
    DifficultyMessage[difficultyKey];

  // スコアに基づいてメッセージを取得する関数
  const getResultMessage = (percentage: number): string => {
    if (percentage === 100) {
      return ResultMessage.PERFECT;
    } else if (percentage >= 66) {
      return ResultMessage.EXCELLENT;
    } else if (percentage >= 33) {
      return ResultMessage.GOOD;
    } else {
      return ResultMessage.NEEDS_IMPROVEMENT;
    }
  };

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
