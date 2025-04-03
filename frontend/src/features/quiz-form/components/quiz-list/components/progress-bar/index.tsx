import React from "react";

interface Props {
  answeredCount: number;
  questionCount: number;
}

export const ProgressBar: React.FC<Props> = ({
  answeredCount,
  questionCount,
}) => {
  return (
    <div className="mb-16 mx-4">
      <div className="w-full bg-gray-100 rounded-full h-6 overflow-hidden mb-6">
        <div
          className="bg-emerald-600 h-6 rounded-l-full transition-all duration-500 ease-out"
          style={{
            width: `${(answeredCount / questionCount) * 100}%`,
          }}
        ></div>
      </div>

      <div className="flex justify-between mb-2 font-bold">
        <span className="text-sm">
          {answeredCount} of {questionCount} questions answered
        </span>
        <span className="text-sm font-bold text-emerald-600 font-bold">
          {Math.round((answeredCount / questionCount) * 100)}%
        </span>
      </div>
    </div>
  );
};
