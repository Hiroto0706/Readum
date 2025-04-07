export enum ResultMessage {
  PERFECT = "完璧！あなたは読書の天才です！",
  EXCELLENT = "素晴らしい！かなり深く理解できているね！",
  GOOD = "まずまず。更に上を目指そう！",
  NEEDS_IMPROVEMENT = "改善の余地あり。もう一度チャレンジ！",
}

export const DifficultyMessage = {
  beginner: {
    value: "やさしい 📚",
    style: "bg-amber-500",
  },
  intermediate: {
    value: "ふつう 🧠",
    style: "bg-teal-500",
  },
  advanced: {
    value: "むずかしい🚀",
    style: "bg-violet-500",
  },
} as const;

interface Option {
  A: string;
  B: string;
  C: string;
  D: string;
}

interface Question {
  content: string;
  options: Option;
  answer: string;
  explanation: string;
}

interface Quiz {
  questions: Question[];
}

export interface UserAnswer {
  id: string;
  preview: Quiz;
  selectedOptions: string[];
  difficultyValue: string;
}

export interface Score {
  correct: number;
  total: number;
  percentage: number;
}
