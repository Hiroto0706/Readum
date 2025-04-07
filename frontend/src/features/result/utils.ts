import { ResultMessage, Score, UserAnswer } from "./types";

export const calculateScore = (result: UserAnswer): Score => {
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

// スコアに基づいてメッセージを取得する関数
export const getResultMessage = (percentage: number): string => {
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
