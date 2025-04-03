import { Option } from "@/features/quiz-form/types";
import React from "react";

interface Props {
  qIndex: number;
  options: Option;
  question: string;
  userAnswers: Record<number, string>;
  handleAnswerSelect: (questionIndex: number, answer: string) => void;
  isSubmitted: boolean;
}

export const QuestionCard: React.FC<Props> = ({
  qIndex,
  options,
  question,
  userAnswers,
  handleAnswerSelect,
  isSubmitted,
}) => {
  return (
    <div className="rounded-xl shadow-md overflow-hidden">
      <div className="font-bold text-lg text-white px-2 md:px-6 py-4 bg-emerald-500 flex items-center">
        <div className="relative flex items-center min-w-8 min-h-8">
          <span className="absolute rounded-full bg-white text-emerald-500 min-w-8 min-h-8 block flex justify-center items-center md:mr-2">
            {qIndex + 1}
          </span>
        </div>
        <p className="pl-2">{question}</p>
      </div>

      <div className="space-y-2 py-4 px-2 md:p-6">
        {Object.entries(options).map(([key, value]) => (
          <div key={key}>
            <label
              className={`flex items-center border rounded-lg p-3 cursor-pointer ${
                userAnswers[qIndex] === key
                  ? "bg-emerald-50 border-emerald-500"
                  : "border-gray-300 hover:bg-gray-100"
              } duration-300`}
            >
              <div className="relative flex items-center justify-center">
                <input
                  type="radio"
                  name={`question-${qIndex}`}
                  value={key}
                  checked={userAnswers[qIndex] === key}
                  onChange={() => handleAnswerSelect(qIndex, key)}
                  disabled={isSubmitted}
                  className="appearance-none w-5 md:w-6 h-5 md:h-6 border border-emerald-500 rounded-full checked:border-emerald-500 transition-colors"
                />
                {userAnswers[qIndex] === key && (
                  // ml-1は丸を縦横中央に配置するため
                  <div className="absolute w-3 md:w-4 h-3 md:h-4 bg-emerald-500 rounded-full pointer-events-none"></div>
                )}
              </div>
              <span className="ml-2">{value}</span>
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};
