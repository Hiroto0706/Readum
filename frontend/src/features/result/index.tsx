"use client";

import ShareButton from "@/components/share-link";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import { ResultCard } from "@/features/result/components/resultCard";
import Link from "next/link";
import { ResultMessage, UserAnswer } from "@/features/result/types";

interface Props {
  result: UserAnswer;
}

export const Result: React.FC<Props> = ({ result }) => {
  const [animatedPercentage, setAnimatedPercentage] = useState(0);

  // 正答率を計算
  const calculateScore = () => {
    let correctCount = 0;
    const totalQuestions = result.preview.questions.length;

    result.preview.questions.forEach((question, index) => {
      if (result.selected_options[index] === question.answer) {
        correctCount++;
      }
    });

    return {
      correct: correctCount,
      total: totalQuestions,
      percentage: Math.round((correctCount / totalQuestions) * 100),
    };
  };

  const score = calculateScore();

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
          <div className="mb-6 font-bold">
            {/* 📚: amber, 🧠 : teal , 🚀 : violet */}
            <span className="py-2 px-4 bg-amber-500 rounded-full text-white">
              かんたん 📚
            </span>
          </div>
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
            selectedOptions={result.selected_options}
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
