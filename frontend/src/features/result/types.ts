export enum ResultMessage {
  PERFECT = "完璧！あなたは読書の天才です！",
  EXCELLENT = "素晴らしい！かなり深く理解できているね！",
  GOOD = "まずまず。更に上を目指そう！",
  NEEDS_IMPROVEMENT = "改善の余地あり。もう一度チャレンジ！",
}

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
  selected_options: string[];
}
