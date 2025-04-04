import Image from "next/image";
import React from "react";
import { QuizResponse } from "@/features/quiz-form/types";
import { ProgressBar } from "@/features/quiz-form/components/quiz-list/components/progress-bar";
import { SubmitButton } from "@/features/quiz-form/components/quiz-list/components/submit-button";
import { QuestionCard } from "@/features/quiz-form/components/quiz-list/components/question-card";

interface Props {
  quizResponse: QuizResponse;
  userAnswers: Record<number, string>;
  handleAnswerSelect: (questionIndex: number, answer: string) => void;
  handleSubmitAnswer: () => Promise<void>;
  isSubmitted: boolean;
}

export const QuizList: React.FC<Props> = ({
  quizResponse,
  userAnswers,
  handleAnswerSelect,
  handleSubmitAnswer,
  isSubmitted,
}) => {
  const questionCount = quizResponse.preview.questions.length;
  const answeredCount = Object.keys(userAnswers).length;

  return (
    <div className="pt-8 mx-2">
      <h2 className="text-xl font-bold flex items-center text-emerald-500 mb-6">
        <Image
          src="/icons/star.svg"
          alt="Star icon"
          width={20}
          height={20}
          className="mr-2"
        />
        クイズに回答しよう！
      </h2>

      <div className="space-y-6 mb-16">
        {quizResponse.preview.questions.map((question, qIndex) => (
          <QuestionCard
            key={qIndex}
            qIndex={qIndex}
            options={question.options}
            question={question.content}
            userAnswers={userAnswers}
            handleAnswerSelect={handleAnswerSelect}
            isSubmitted={isSubmitted}
          />
        ))}
      </div>

      <ProgressBar
        answeredCount={answeredCount}
        questionCount={questionCount}
      />

      <SubmitButton
        userAnswers={userAnswers}
        handleSubmitAnswer={handleSubmitAnswer}
        questionCount={questionCount}
        isSubmitted={isSubmitted}
      />
    </div>
  );
};
