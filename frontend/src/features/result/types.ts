// 型定義
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
