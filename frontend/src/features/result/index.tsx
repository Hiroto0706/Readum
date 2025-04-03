import ShareButton from "@/components/share-link";
import Image from "next/image";
import React from "react";
import { ResultCard } from "./components/resultCard";
import Link from "next/link";
import { UserAnswer } from "./types";

interface Props {
  result: UserAnswer;
}

export const Result: React.FC<Props> = ({ result }) => {
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

      <div className="rounded-lg border border-gray-300 text-center truncate mb-8 shadow">
        <div className="w-full bg-emerald-500 text-white font-bold text-xl md:text-2xl py-4">
          完璧！あなたは読書の天才です！
        </div>
        <div className="p-6 flex flex-col justify-center items-center">
          <div className="w-36 h-36 bg-emerald-100 rounded-full flex justify-center items-center">
            <p className="font-bold text-4xl text-white w-28 h-28 rounded-full bg-emerald-500 flex justify-center items-center">
              {score.percentage}%
            </p>
          </div>
          <p className="mt-2 space-x-2 flex justify-center items-center">
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
