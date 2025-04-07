import { Option } from "@/features/quiz-form/types";
import Image from "next/image";
import React from "react";

interface Props {
  qIndex: number;
  options: Option;
  question: string;
  answer: string;
  explanation: string;
  selectedOptions: string[];
}

export const ResultCard: React.FC<Props> = ({
  qIndex,
  options,
  question,
  answer,
  explanation,
  selectedOptions,
}) => {
  const isCorrected = selectedOptions[qIndex] === answer;

  return (
    <div className="rounded-xl shadow-md overflow-hidden">
      <div
        className={`font-bold text-lg text-white px-2 md:px-6 py-4 flex items-center ${
          isCorrected ? "bg-green-500" : "bg-red-500"
        }`}
      >
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
              className={`flex items-center border rounded-lg p-3 ${
                selectedOptions[qIndex] === key
                  ? `${
                      isCorrected
                        ? "border-green-500 bg-green-50"
                        : "border-red-500 bg-red-50"
                    }`
                  : key === answer && !isCorrected
                  ? "border-green-500 bg-green-50"
                  : "border-gray-300"
              } duration-300`}
            >
              <div className="relative flex items-center justify-center">
                <input
                  type="radio"
                  name={`question-${qIndex}`}
                  value={key}
                  checked={selectedOptions[qIndex] === key}
                  disabled
                  readOnly
                  className={`appearance-none w-5 md:w-6 h-5 md:h-6 border rounded-full transition-colors ${
                    isCorrected
                      ? "checked:border-green-500"
                      : key === answer && !isCorrected
                      ? "border-green-500"
                      : "checked:border-red-500"
                  }`}
                />
                {selectedOptions[qIndex] === key && (
                  <div
                    className={`absolute w-3 md:w-4 h-3 md:h-4 rounded-full pointer-events-none ${
                      isCorrected ? "bg-green-500" : "bg-red-500"
                    }`}
                  ></div>
                )}
                {key === answer &&
                  !isCorrected &&
                  selectedOptions[qIndex] !== key && (
                    <div className="absolute w-3 md:w-4 h-3 md:h-4 rounded-full pointer-events-none bg-green-500"></div>
                  )}
              </div>
              <span className="ml-2 text-base">{value}</span>
            </label>
          </div>
        ))}

        <div className="mt-6 p-4 border border-gray-300 rounded-lg">
          <p className="mb-2 font-bold flex items-center">
            <Image
              src="/icons/star.svg"
              alt="Star icon"
              width={16}
              height={16}
              className="mr-1"
            />
            解説
          </p>
          {explanation}
        </div>
      </div>
    </div>
  );
};
